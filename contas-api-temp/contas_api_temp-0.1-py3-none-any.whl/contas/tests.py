"""
Testes a serem utilizadas em contas/views.py
"""
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth.models import User

from contas.models import Conta


class ContaListAllTest(APITestCase):
    """
    Módulo de teste para a listagem de todas as contas.
    Testa o ContaList view em contas/views.py
    """
    def setUp(self):
        """
        Cria o banco necessário para rodar os testes
        """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        # Cria contas
        Conta.objects.create(
            name="Conta Corrente",
            description="Transações da conta corrente do banco: ABC",
            owner=User.objects.get(username='joao'))
        Conta.objects.create(
            name="Investimentos",
            description="Investimentos feito pela corretora: XYZ",
            owner=User.objects.get(username='joao'))

    def test_get_all_contas(self):
        """
        Verifica se está listando as contas corretamente
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('conta-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conta.objects.count(), 2)


class ContaGetUnicTest(APITestCase):
    """
    Módulo de teste para selecionar uma única conta.
    Testa o ContaDetail view em contas/views.py
    """
    def setUp(self):
        """
        Cria o banco necessário para rodar os testes
        """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria contas
        self.contacorrente = Conta.objects.create(
            name="Conta Corrente",
            description="Transações da conta corrente do banco: ABC",
            owner=User.objects.get(username='joao'))
        self.cartaocredito = Conta.objects.create(
            name="Cartão de Crédito",
            description="Fatura do cartão de crédito",
            owner=User.objects.get(username='joao'))
        self.investimentos = Conta.objects.create(
            name="Investimentos",
            description="Investimentos feito pela corretora: XYZ",
            owner=User.objects.get(username='maria'))

    def test_get_valid_conta(self):
        """
        Verifica se está selecionando as contas corretamente
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('conta-detail',
                                           kwargs={'pk':
                                                   self.cartaocredito.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conta.objects.get(pk=self.cartaocredito.pk).name,
                         "Cartão de Crédito")

    def test_get_invalid_conta(self):
        """
        Verifica se está retornando 404 quando se
        seleciona objetos não existentes
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('conta-detail',
                                           kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_forbidden_conta(self):
        """
        Verifica se está bloqueando a seleção por usuários sem
        permissão.
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('conta-detail',
                                           kwargs={'pk':
                                                   self.investimentos.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ContaNewTest(APITestCase):
    """
    Módulo de teste para a criação de uma nova conta.
    Testa o ContaList view em contas/views.py
    """
    def setUp(self):
        """
        Cria o banco necessário para rodar os testes
        """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        # requests de contas
        self.valid_payload = {
            'name': 'Conta',
            'description': 'Descrição da conta.'
        }
        self.invalid_payload = {
            'name': '',
            'description': ''
        }

    def test_create_valid_conta(self):
        """
        Verifica se estão sendo criados objetos corretamente
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(reverse('conta-list'),
                                    self.valid_payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Conta.objects.count(), 1)
        self.assertEqual(Conta.objects.get().owner.username, 'joao')
        self.assertEqual(Conta.objects.get().name, 'Conta')

    def test_create_invalid_conta(self):
        """
        Verifica se está retornando má requisição se estiver
        tentando criar objetos não permitidos.
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(reverse('conta-list'),
                                    self.invalid_payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_forbiden_cont(self):
        """
        Verifica se está bloqueando a tentativa de criar
        objetos por usuários não logados.
        """
        response = self.client.post(reverse('conta-list'),
                                    self.valid_payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ContaUpdateTest(APITestCase):
    """
    Módulo de teste para a atualização de uma conta existente.
    Testa o ContaDetail view em contas/views.py
    """
    def setUp(self):
        """
        Cria o banco necessário para rodar os testes
        """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria contas
        self.investimentos = Conta.objects.create(
            name="Investimentos",
            description="Investimentos feito pela corretora: XYZ",
            owner=User.objects.get(username='maria'))
        # requests de contas
        self.valid_payload = {
            'name': 'Conta',
            'description': 'Descrição da conta.'
        }
        self.invalid_payload = {
            'name': '',
            'description': ''
        }

    def test_update_valid_conta(self):
        """
        Verifica se estão sendo atualizados objetos corretamente
        """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.put(
            reverse('conta-detail', kwargs={'pk': self.investimentos.pk}),
            self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conta.objects.get(pk=self.investimentos.pk).name,
                         'Conta')

    def test_update_invalid_conta(self):
        """
        Verifica se está retornando má requisição se estiver tentando
        atualizar objetos de maneira não permitida
        """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.put(
            reverse('conta-detail', kwargs={'pk': self.investimentos.pk}),
            self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_not_allowed_conta(self):
        """
        Verifica se está bloqueando a tentativa de atualizar
        objetos por usuários não permitidos
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(
            reverse('conta-detail', kwargs={'pk': self.investimentos.pk}),
            self.valid_payload, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_forbiden_cont(self):
        """
        Verifica se está bloqueando a tentativa de atualizar
        objetos por usuários não logados
        """
        response = self.client.post(
            reverse('conta-detail', kwargs={'pk': self.investimentos.pk}),
            self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ContaDeleteTest(APITestCase):
    """
    Módulo para deletar uma conta existente.
    Testa o ContaDetail view em contas/views.py
    """
    def setUp(self):
        """
        Cria o banco necessário para rodar os testes
        """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria contas
        self.investimentos = Conta.objects.create(
            name="Investimentos",
            description="Investimentos feito pela corretora: XYZ",
            owner=User.objects.get(username='maria'))

    def test_delete_conta_valid(self):
        """
        Verifica se os objetos estão sendo deletados
        corretamente
        """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.delete(
            reverse('conta-detail',
                    kwargs={'pk': self.investimentos.pk}))
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_delete_conta_invalid(self):
        """
        Verifica se está retornando 404 quando se seleciona objetos
        não existentes
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.delete(
            reverse('conta-detail', kwargs={'pk': 20}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_allowed_conta(self):
        """
        Verifica se está bloqueando a tentativa de deletar
        objetos por usuários não permitidos
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.delete(
            reverse('conta-detail',
                    kwargs={'pk': self.investimentos.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_forbiden_cont(self):
        """
        Verifica se está bloqueando a tentativa de deletar
        objetos por usuários não logados
        """
        response = self.client.delete(
            reverse('conta-detail',
                    kwargs={'pk': self.investimentos.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
