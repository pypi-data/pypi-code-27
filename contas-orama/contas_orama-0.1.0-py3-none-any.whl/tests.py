"""
Testes a serem utilizadas em views.py
"""
import subprocess
import os

from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth.models import User

from contas_orama.models import Conta, Lancamento

# Obtém o diretório onde a API contas_orama foi salva
CONTAS_ORAMA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'contas_orama')

# Testa o pylint
# Exceções: W0221, W0223, R0901, R0903
subprocess.call('pylint --load-plugins pylint_django \
                --disable=W0221,W0223,R0901,R0903 ' + CONTAS_ORAMA_DIR,
                shell=True)

# Testa o pycodestyle
subprocess.call('pycodestyle ' + CONTAS_ORAMA_DIR, shell=True)


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


class LancamentoRetrieveContaTest(APITestCase):
    """
    Módulo de teste para selecionar uma única conta para fazer um
    novo lançamento.
    Testa o LancamentoCreate view em contas/views.py
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

        response = self.client.get(
            reverse('lancamento-create', kwargs={'pk':
                                                 self.cartaocredito.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conta.objects.get(pk=self.cartaocredito.pk).name,
                         "Cartão de Crédito")

    def test_get_invalid_conta(self):
        """
        Verifica se está retornando 404 quando se seleciona objetos
        não existentes
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('lancamento-create',
                                           kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_forbidden_conta(self):
        """
        Verifica se está bloqueando a seleção por usuários sem permissão
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(
            reverse('lancamento-create', kwargs={'pk':
                                                 self.investimentos.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LancamentoNewTest(APITestCase):
    """
    Módulo de teste para a criação de um novo lançamento.
    Testa o LancamentoCreate view em lancamentos/views.py
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
        Conta.objects.create(
            name="Conta Corrente",
            description="",
            owner=User.objects.get(username='joao'))
        # requests de lancamentos
        self.valid_payload = {
            'name': 'Salário',
            'value': 10.00
        }
        self.invalid_payload = {
            'name': '',
            'value': 10000.00
        }

    def test_create_valid_conta(self):
        """ Verifica se estão sendo criados objetos corretamente """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(
            reverse('lancamento-create',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk}),
            self.valid_payload,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Lancamento.objects.count(), 1)
        self.assertEqual(Lancamento.objects.get().owner.username, 'joao')
        self.assertEqual(Lancamento.objects.get().conta.name, 'Conta Corrente')
        self.assertEqual(Lancamento.objects.get().name, 'Salário')

    def test_create_invalid_conta(self):
        """
        Verifica se está retornando má requisição se estiver tentando criar
        objetos não permitidos
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(
            reverse('lancamento-create',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk}),
            self.invalid_payload,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_not_login_conta(self):
        """
        Verifica se está bloqueando a tentativa de criar objetos por usuários
        não logados
        """
        response = self.client.post(
            reverse('lancamento-create',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk}),
            self.valid_payload,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_forbiden_conta(self):
        """
        Verifica se está bloqueando a tentativa de criar objetos por usuários
        não permitidos
        """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.post(
            reverse('lancamento-create',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk}),
            self.valid_payload,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LancamentoGetUnicTest(APITestCase):
    """
    Módulo de teste para selecionar um único lançamento.
    Testa o LancamentoDetail view em contas/views.py
    """
    def setUp(self):
        """ Cria o banco necessário para rodar os testes """
        # Criar usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria Contas
        Conta.objects.create(
            name="Conta Corrente",
            description="Transações da conta corrente do banco: ABC",
            owner=User.objects.get(username='joao'))
        Conta.objects.create(
            name="Conta Corrente",
            description="Transações da conta corrente do banco: 123",
            owner=User.objects.get(username='maria'))
        # Cria Lançamentos
        self.padaria = Lancamento.objects.create(
            name='Padaria', lanc_tp=2, value=10.00,
            owner=User.objects.get(username='joao'),
            conta=Conta.objects.get(name='Conta Corrente',
                                    owner__username='joao'))
        self.salario = Lancamento.objects.create(
            name='Salário', value=10000.00,
            owner=User.objects.get(username='maria'),
            conta=Conta.objects.get(name='Conta Corrente',
                                    owner__username='maria'))

    def test_get_valid_lancamento(self):
        """ Verifica se está selecionando os lançamentos corretamente """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('lancamento-detail',
                                           kwargs={'pk': self.padaria.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lancamento.objects.get(pk=self.padaria.pk).name,
                         "Padaria")

    def test_get_invalid_lancamento(self):
        """ Verifica se está retornando 404 quando se seleciona objetos
        não existentes """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('conta-detail',
                                           kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_forbidden_lancamento(self):
        """ Verifica se está bloqueando a seleção por usuários sem permissão
        """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('lancamento-detail',
                                           kwargs={'pk': self.salario.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LancamentoUpdateTest(APITestCase):
    """
    Módulo de teste para a atualização de um lancamento existente.
    Testa o LancamentoDetail view em lancamentos/views.py
    """
    def setUp(self):
        """ Cria o banco necessário para rodar os testes """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria contas
        Conta.objects.create(
            name="Investimentos", description='',
            owner=User.objects.get(username='maria'))
        # Cria lançamentos
        self.ativo = Lancamento.objects.create(
            name="Compra de Ativo", lanc_tp=2, value=1000.00,
            owner=User.objects.get(username='maria'),
            conta=Conta.objects.get(name='Investimentos'))
        # requests de lançamentos
        self.valid_payload = {
            'name': 'Compra',
            'value': 10000.00
        }
        self.invalid_payload = {
            'name': '',
            'description': 0.00
        }

    def test_update_valid_lancamento(self):
        """ Verifica se estão sendo atualizados objetos corretamente """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.put(reverse('lancamento-detail',
                                           kwargs={'pk': self.ativo.pk}),
                                   self.valid_payload,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lancamento.objects.get(pk=self.ativo.pk).name,
                         'Compra')

    def test_update_invalid_lancamento(self):
        """ Verifica se está retornando má requisição se estiver
        tentando atualizar objetos de maneira não permitida """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.put(reverse('lancamento-detail',
                                           kwargs={'pk': self.ativo.pk}),
                                   self.invalid_payload,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_not_allowed_conta(self):
        """ Verifica se está bloqueando a tentativa de atualizar objetos
        por usuários não permitidos """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(reverse('lancamento-detail',
                                            kwargs={'pk': self.ativo.pk}),
                                    self.valid_payload,
                                    format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_forbiden_conta(self):
        """ Verifica se está bloqueando a tentativa de atualizar objetos
        por usuários não logados """
        response = self.client.post(reverse('lancamento-detail',
                                            kwargs={'pk': self.ativo.pk}),
                                    self.valid_payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LancamentoDeleteTest(APITestCase):
    """
    Módulo para testar o delete de um lançamento existente.
    Testa o LancamentoDetail view em lancamentos/views.py
    """
    def setUp(self):
        """ Cria o banco necessário para rodar os testes """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria contas
        Conta.objects.create(
            name="Investimentos",
            description="Detalhamento investimentos feito pela corretora: XYZ",
            owner=User.objects.get(username='maria'))
        # Cria lançamentos
        self.ativo = Lancamento.objects.create(
            name="Compra de Ativo", lanc_tp=2, value=1000.00,
            owner=User.objects.get(username='maria'),
            conta=Conta.objects.get(name='Investimentos'))

    def test_delete_valid_lancamento(self):
        """ Verifica se os objetos estão sendo deletados corretamente """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.delete(reverse('lancamento-detail',
                                              kwargs={'pk': self.ativo.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_lancamento(self):
        """ Verifica se está retornando 404 quando se seleciona objetos não
        existentes """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.delete(reverse('lancamento-detail',
                                              kwargs={'pk': 20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_forbiden_lancamento(self):
        """ Verifica se está bloqueando a tentativa de deletar objetos por
        usuários não permitidos """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.delete(reverse('lancamento-detail',
                                              kwargs={'pk': self.ativo.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_not_log_lancamento(self):
        """ Verifica se está bloqueando a tentativa de deletar objetos por
        usuários não logados """
        response = self.client.delete(reverse('conta-detail',
                                              kwargs={'pk': self.ativo.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LancamentoListTest(APITestCase):
    """
    Módulo de teste para a listagem dos lancamentos.
    Testa o LancamentoList view em lancamento/views.py
    """
    def setUp(self):
        """ Cria o banco necessário para rodar os testes """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria contas
        Conta.objects.create(
            name="Conta Corrente",
            description="Transações da conta corrente do banco: ABC",
            owner=User.objects.get(username='joao'))
        # Cria lancamentos
        Lancamento.objects.create(
            name="Padaria", date="2018-07-10", lanc_tp=2, value=20.00,
            owner=User.objects.get(username='joao'),
            conta=Conta.objects.get(name='Conta Corrente'))
        Lancamento.objects.create(
            name="Farmácia", date="2018-07-08", lanc_tp=2, value=65.00,
            owner=User.objects.get(username='joao'),
            conta=Conta.objects.get(name='Conta Corrente'))
        Lancamento.objects.create(
            name="Salário", date="2018-07-01", value=65.00,
            owner=User.objects.get(username='joao'),
            conta=Conta.objects.get(name='Conta Corrente'))

    def test_list_lancamentos(self):
        """ Verifica se está listando os lancamentos corretamente """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        date_ini = "2018-07-01"
        date_end = "2018-08-01"

        response = self.client.get(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': date_ini,
                            'end': date_end}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lancamento.objects.count(), 3)
        self.assertEqual(Lancamento.objects.get_balance(
            date_ini=date_ini, date_end=date_end,
            conta_id=Conta.objects.get(
                owner__username='joao').pk), -20.00)

    def test_list_ii_lancamentos(self):
        """ Outro teste para ver se Lancamento.objects.get_balance funciona
        adequadamente """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        date_ini = "2018-07-07"
        date_end = "2018-08-01"

        response = self.client.get(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': date_ini,
                            'end': date_end}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lancamento.objects.count(), 3)
        self.assertEqual(Lancamento.objects.get_balance(
            date_ini=date_ini, date_end=date_end,
            conta_id=Conta.objects.get(
                owner__username='joao').pk), -85.00)

    def test_list_iii_lancamentos(self):
        """ Outro teste diferente para Lancamento.objects.get_balance """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        date_ini = "2018-07-01"
        date_end = "2018-07-07"

        response = self.client.get(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': date_ini,
                            'end': date_end}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lancamento.objects.count(), 3)
        self.assertEqual(Lancamento.objects.get_balance(
            date_end=date_end,
            conta_id=Conta.objects.get(
                owner__username='joao').pk), 65.00)

    def test_list_forbiden_lancamentos(self):
        """ Verifica se está bloqueando a tentativa de listar objetos de outros
        usuários """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.get(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': "2018-07-01",
                            'end': "2018-08-01"}), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_not_login_lancamentos(self):
        """ Verifica se está bloqueando a tentativa de listar objetos de
        usuários não logados """
        response = self.client.get(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': "2018-07-01",
                            'end': "2018-08-01"}), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DateFilterNewTest(APITestCase):
    """
    Módulo de teste para a criação de um novo DateFilterSerializer
    (lancamentos/serializers.py).
    Testa o LancamentoList view em lancamentos/views.py
    """
    def setUp(self):
        """ Cria o banco necessário para rodar os testes """
        # Cria usuários
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")
        # Cria contas
        Conta.objects.create(
            name="Conta Corrente", description="",
            owner=User.objects.get(username='joao'))
        # Cria lancamentos
        Lancamento.objects.create(
            name="Padaria", date="2018-07-10", lanc_tp=2, value=20.00,
            owner=User.objects.get(username='joao'),
            conta=Conta.objects.get(name='Conta Corrente'))
        Lancamento.objects.create(
            name="Farmácia", date="2018-08-08", lanc_tp=2, value=65.00,
            owner=User.objects.get(username='joao'),
            conta=Conta.objects.get(name='Conta Corrente'))
        # requests do dateFilter
        self.valid_payload = {
            'data_ini': "2018-07-01",
            'data_end': "2018-07-13"
        }
        self.invalid_payload = {
            'data_ini': "2018-07-07",
            'data_end': "2018-07-01"
        }

    def test_create_valid_date(self):
        """ Verifica se está sendo direcionado URL corretamente, a partir dos
        dados inseridos no form """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': "2018-08-01",
                            'end': "2018-08-30"}),
            self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_invalid_date(self):
        """ Verifica se está retornando má requisição se estiver tentando
        criar dateFilter não permitidos """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.post(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': "2018-08-01",
                            'end': "2018-08-30"}),
            self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_not_login_date(self):
        """ Verifica se está bloqueando a tentativa de criar dateFilter
        por usuários não logados """
        response = self.client.post(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': "2018-08-01",
                            'end': "2018-08-30"}),
            self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_forbiden_date(self):
        """ Verifica se está bloqueando a tentativa de acesso por usuários
        não donos da conta """
        user = User.objects.get(username='maria')
        self.client.force_login(user)

        response = self.client.post(
            reverse('lancamento-list',
                    kwargs={'pk': Conta.objects.get(
                        owner__username='joao').pk,
                            'ini': "2018-08-01",
                            'end': "2018-08-30"}),
            self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UsuarioListAllTest(APITestCase):
    """
    Módulo de teste para a listagem de todos os usuários.
    Testa o UserList view em usuarios/views.py
    """
    def setUp(self):
        """ Cria o banco de dados """
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")

    def test_get_all_users(self):
        """ Listagem de todos os usuários """
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
        """ Cria o banco de dados """
        User.objects.create(
            username="joao", password="123456ab")
        User.objects.create(
            username="maria", password="123456ab")

    def test_get_valid_usuario(self):
        """ Verifica se está selecionando os usuários corretamente """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(
            reverse('user-detail',
                    kwargs={'pk': User.objects.get(username='joao').pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_usuario(self):
        """ Verifica se está retornando 403 quando se seleciona
        objetos não permitidos """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        response = self.client.get(reverse('user-detail', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_forbiden_usuario(self):
        """ Verifica se está bloqueando a seleção por
        usuários sem permissão """
        user = User.objects.get(username='joao')
        self.client.force_login(user)

        self.client.login(username=user.username, password='123456ab')
        response = self.client.get(
            reverse('user-detail',
                    kwargs={'pk': User.objects.get(username='maria').pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
