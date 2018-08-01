"""
Views para os lancamentos
"""
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from contas.models import Conta
from contas.serializers import ContaSerializer

from lancamentos.models import Lancamento
from lancamentos.serializers import LancamentoSerializer, DateFilterSerializer
from lancamentos.permissions import IsOwner
from lancamentos.pagination import LancamentoPagination


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
        # conta_name - É o nome da conta à qual os lancamentos pertencem
        # inicio - É a data inicial da amostragem
        # saldo_inicio - É o saldo da conta na data início
        # fim - É a data final da amostragem
        # saldo_fim - É o saldo da conta na data fim
        conta_info = {'conta_name': get_object_or_404(
            Conta.objects.all(), pk=self.kwargs['pk']).name,
                      'inicio': self.kwargs['ini'],
                      'saldo_inicio': Lancamento.objects.get_balance(
                          date_end=self.kwargs['ini'],
                          conta_id=self.kwargs['pk']),
                      'fim': self.kwargs['end'],
                      'saldo_fim': Lancamento.objects.get_balance(
                          date_ini=self.kwargs['ini'],
                          date_end=self.kwargs['end'],
                          conta_id=self.kwargs['pk'])}

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
