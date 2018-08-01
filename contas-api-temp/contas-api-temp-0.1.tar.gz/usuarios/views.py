"""
Views para listar e criar usuários
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from usuarios.serializers import UserSerializer
from usuarios.permissions import IsUser


@api_view(['GET'])
def api_root(request):
    """
    Primeiro view da API (view raiz)
    """
    return Response({
        'contas': reverse('conta-list', request=request),
        'usuarios': reverse('user-list', request=request),
    })


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
