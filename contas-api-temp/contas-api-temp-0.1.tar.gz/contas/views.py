"""
Views para os lancamentos
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from contas.models import Conta
from contas.serializers import ContaSerializer
from contas.permissions import IsOwner


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
    Também retorna o link para acessar a URL lancamento-list corretamente
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
