"""
Views para a API
"""
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from contas_orama.models import Conta, Lancamento
from contas_orama.serializers import (ContaSerializer, LancamentoSerializer,
                                      UserSerializer, DateFilterSerializer, )
from contas_orama.permissions import IsOwner, IsUser
from contas_orama.pagination import LancamentoPagination


@api_view(['GET'])
def api_root(request):
    """
    Primeiro view da API (view raiz)
    """
    return Response({
        'contas': reverse('conta-list', request=request),
        'usuarios': reverse('user-list', request=request),
    })


class ContaList(generics.ListCreateAPIView):
    """
    View para criação e listagem de contas
    """
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

    # Permissão para que somente usuários autenticados consigam ter acesso
    # ao view de listagem de contas.
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, pk=None):
        """
        Função create está sendo sobrescrita para que após a postagem seja
        possível redirecionar automaticamente para a url conta-list
        """
        serializer = ContaSerializer(data=request.data,
                                     context={'request': request})
        if serializer.is_valid():
            # Salva automaticamente o campo owner de utilizando o usuário
            # logado
            serializer.save(owner=self.request.user)

            # Redireiona após a postagem para a página da conta-list
            return HttpResponseRedirect(reverse('conta-list'))
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Filtra para que o usuário somente veja as próprias contas
        """
        return Conta.objects.filter(owner=self.request.user)


class ContaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View que Retorna, Atualiza e Deleta uma conta
    Também retorna o link para acessar ver o extrato e
    fazer um novo lançamento.
    """
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

    # Permissão para que somente usuários logados e donos da conta
    # possam ter acesso a esta URL
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def retrieve(self, request, pk=None):
        """
        Função retrieve foi sobrescrita para poder retornar um link funcional
        para lancamento-list
        """
        queryset = Conta.objects.all()
        conta = get_object_or_404(queryset, pk=pk)

        # Checa se o usuário tem permissão para acessar o objeto conta
        self.check_object_permissions(self.request, conta)
        serializer = ContaSerializer(conta, context={'request': request})

        # Define as datas: inicial e final para entrar na url de
        # lancamento-list.
        # Foi definido um intervalo padrão entre o dia atual,
        # e o primeiro dia do mês atual.
        data_ini_padrao = now().replace(day=1).strftime('%Y-%m-%d')
        data_end_padrao = now().strftime('%Y-%m-%d')

        update_dict = {'ver-extrato': reverse('lancamento-list',
                                              kwargs={'pk': pk,
                                                      'ini': data_ini_padrao,
                                                      'end': data_end_padrao},
                                              request=request),
                       'fazer-novo-lancamento': reverse('lancamento-create',
                                                        kwargs={'pk': pk},
                                                        request=request)}
        update_dict.update(serializer.data)

        return Response(update_dict)


class LancamentoCreate(mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    """
    View que permite a postagem de um novo lançamento utilizando
    a conta presente na URL
    """
    queryset = Lancamento.objects.all()
    serializer_class = LancamentoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, *args, **kwargs):
        """
        Chamada de retrieve
        """
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        """
        Seleciona o objeto conta com o id dado pela URL
        """
        queryset = Conta.objects.all()
        conta = get_object_or_404(queryset, pk=pk)

        # Checa se o usuário tem as permissões necessárias para
        # acessar o objeto conta
        self.check_object_permissions(self.request, conta)
        serializer = ContaSerializer(conta, context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Chamadade create
        """
        return self.create(request, *args, **kwargs)

    def create(self, request, pk=None):
        """
        Cria o objeto lançamento
        """
        # Seleciona a conta onde o lancamento será realizados
        conta = get_object_or_404(Conta.objects.all(),
                                  pk=self.kwargs.get('pk'))

        # Checa se o usuário tem as permissões necessárias para
        # acessar o objeto conta
        self.check_object_permissions(self.request, conta)
        serializer = LancamentoSerializer(data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            # Salva o lancamento utilizando automaticamente o campo owner
            # e conta_id utilizando o request e a URL respectivamente
            serializer.save(owner=self.request.user,
                            conta_id=self.kwargs.get('pk'))

            # Redireciona após a postagem para a página da própria conta
            return HttpResponseRedirect(
                reverse('conta-detail',
                        kwargs={'pk': self.kwargs.get('pk')}))
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LancamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View que Retorna, Atualiza e Deleta um lançamento
    """
    queryset = Lancamento.objects.all()
    serializer_class = LancamentoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)


class LancamentoList(generics.ListCreateAPIView):
    """
    View que filtra todos os lançamentos feitos durante um período e em
    em uma daterminada conta, ambos parâmetros dados pela URL.

    Também retorna parâmetros julgados necessários para o front-end:
    o nome da conta, a data inicial e final do período e
    os saldos inicial, do período e o final.

    O view também permite a entrada de um novo período dado pelo usuário,
    redirecionando-o para uma URL com novas datas.
    """
    serializer_class = DateFilterSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def list(self, request, pk=None, ini=None, end=None):
        """
        Lista os lançamentos da conta.pk = pk durante o período
        entre data = ini e data = end

        Mostra o saldo anterior e o final do período.
        """
        queryset = self.get_queryset()
        serializer = LancamentoSerializer(queryset,
                                          many=True,
                                          context={'request': request})

        # Preenchimento do dict com valores a serem utilizados na renderização
        # de lancamento-list
        # conta_nome - É o nome da conta à qual os lancamentos pertencem
        # inicio - É a data inicial da amostragem
        # fim - É a data final da amostragem
        # saldo_inicial - É o saldo da conta na data início
        # saldo_periodo - É o saldo da conta durante o período
        # saldo_final - É o saldo da conta na data fim
        saldo_inicio = Lancamento.objects.get_balance(
            date_end=self.kwargs['ini'],
            conta_id=self.kwargs['pk'])

        saldo_interv = Lancamento.objects.get_balance(
            date_ini=self.kwargs['ini'],
            date_end=self.kwargs['end'],
            conta_id=self.kwargs['pk'])

        conta_info = {'conta_nome': get_object_or_404(
            Conta.objects.all(), pk=self.kwargs['pk']).name,
                      'inicio': self.kwargs['ini'],
                      'fim': self.kwargs['end'],
                      'saldo_inicial': saldo_inicio,
                      'saldo_periodo': saldo_interv,
                      'saldo_fim': saldo_inicio + saldo_interv}

        # Retornar a lista de objetos 'paginada'
        # Paginação:
        # http://www.django-rest-framework.org/api-guide/pagination/#pagination
        # "Django provides a few classes that help you manage paginated data –
        # that is, data that’s split across several pages, with
        # “Previous/Next” links.""

        # get_paginated_response foi sobrescrita em contas/pagination.py
        # Sobrescrição feita para incluir o dict conta_info na paginação
        paginator = LancamentoPagination()
        page = paginator.paginate_queryset(serializer.data, request)
        if page is not None:
            return paginator.get_paginated_response(page, conta_info)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Filtra a lista de lançamentos utilizando as datas (inicial e final)
        e a conta dados na url
        """
        conta = get_object_or_404(Conta.objects.all(), pk=self.kwargs['pk'])

        # Checa se o usuário é dono da conta e tem permissão
        # para ter acesso a mesma.
        self.check_object_permissions(self.request, conta)
        ini = self.kwargs['ini']
        end = self.kwargs['end']
        return Lancamento.objects.filter(date__gte=ini,
                                         date__lte=end,
                                         conta=conta).order_by('date')

    def create(self, request, pk=None, ini=None, end=None):
        """
        Posta as novas data iniciais e finais
        redireciona para a URL desejada utilizando as datas
        """
        conta = get_object_or_404(Conta.objects.all(), pk=self.kwargs['pk'])
        # Checa se o usuário é dono da conta e tem permissão
        # para ter acesso a mesma.
        self.check_object_permissions(self.request, conta)

        serializer = DateFilterSerializer(data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            ini = serializer.validated_data['data_ini'].strftime('%Y-%m-%d')
            end = serializer.validated_data['data_end'].strftime('%Y-%m-%d')
            return HttpResponseRedirect(
                reverse('lancamento-list',
                        kwargs={'pk': self.kwargs.get('pk'),
                                'ini': ini,
                                'end': end}))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    """
    View para a listagem dos usuários.
    No entanto, filtra para que os usuários somente possam ver a
    si mesmos.

    Poderia adicionar que superusuários pudessem ver todos.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Permissão para que somente usuários autenticados consigam ter
    # acesso ao view de listagem de usuários
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Filtra para que o usuário somente veja a si próprio
        """
        return User.objects.filter(username=self.request.user).order_by('id')


class UserDetail(generics.RetrieveAPIView):
    """
    View para a visualização detalhada dos usuários.
    Usuário somente pode ver a própria página
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Permissão para que somente usuários logados possam
    # acessar o próprio view
    permission_classes = (permissions.IsAuthenticated, IsUser,)
