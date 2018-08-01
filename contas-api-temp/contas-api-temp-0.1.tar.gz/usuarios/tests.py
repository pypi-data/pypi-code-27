"""
Testes a serem utilizadas em usuarios/views.py
"""
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.urls import reverse


class UsuarioListAllTest(APITestCase):
    """
    Módulo de teste para a listagem de todos os usuários.
    Testa o UserList view em usuarios/views.py
    """
    def setUp(self):
        """
        Cria o banco de dados
        """
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")

    def test_get_all_users(self):
        """
        Listagem de todos os usuários
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('user-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)


class UsuarioGetUnicTest(APITestCase):
    """
    Módulo de teste para selecionar um único usuário.
    Testa o UserDetail view em usuarios/views.py
    """
    def setUp(self):
        """
        Cria o banco de dados
        """
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")

    def test_get_valid_usuario(self):
        """
        Verifica se está selecionando os usuários corretamente
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(
            reverse('user-detail',
                    kwargs={'pk': User.objects.get(username='joao').pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_usuario(self):
        """
        Verifica se está retornando 403 quando se seleciona
        objetos não permitidos
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('user-detail', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_forbiden_usuario(self):
        """
        Verifica se está bloqueando a seleção por
        usuários sem permissão
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        self.client.login(username=user.username, password='123456ab')
        response = self.client.get(
            reverse('user-detail',
                    kwargs={'pk': User.objects.get(username='maria').pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
