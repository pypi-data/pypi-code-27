"""
Models da API
"""
import datetime
import decimal

from django.db import models


class Conta(models.Model):
    """
    Contas dos Usuários
    Ex.: Conta corrente, Investimentos, Cartão de Crédito, etc...
    """
    name = models.CharField('Título da Conta:',
                            max_length=255)
    description = models.TextField('Descrição:',
                                   blank=True,
                                   default='')
    owner = models.ForeignKey('auth.User',
                              related_name='contas',
                              on_delete=models.CASCADE)

    def __str__(self):
        """
        Faz com que a conta string de conta seja igual a
        field name
        """
        return self.name

    class Meta:
        ordering = ["name"]


class LancamentoManager(models.Manager):
    """
    Manager de Lancamento
    Criado para gerar a função get_balance
    """
    def get_balance(self, date_end, conta_id, date_ini=None):
        """
        Função get_balance retorna o saldo durante o período entre date_ini e
        date_end da conta com o id igual a conta_id.

        Caso não seja dado o parâmetro date_ini, o saldo é calculado para
        desde o primeiro lançamento na conta, até o dia anterior ao date_end.
        """
        if date_ini is None:
            lanc_filt_date = self.filter(date__lt=date_end,
                                         conta=conta_id)
        else:
            lanc_filt_date = self.filter(date__gte=date_ini,
                                         date__lte=date_end,
                                         conta=conta_id)

        # Soma dos débitos
        deb_sum = lanc_filt_date.filter(
            lanc_tp=1).aggregate(models.Sum('value'))
        if deb_sum['value__sum'] is None:
            deb_sum['value__sum'] = decimal.Decimal(0.00)

        # Soma dos créditos
        cre_sum = lanc_filt_date.filter(
            lanc_tp=2).aggregate(models.Sum('value'))
        if cre_sum['value__sum'] is None:
            cre_sum['value__sum'] = decimal.Decimal(0.00)

        return deb_sum['value__sum'] - cre_sum['value__sum']


class Lancamento(models.Model):
    """
    Lancamento dos Usuários
    Ex.: Salário, Compra de Ativos, Padaria, etc...
    """
    Transactions_Choices = (
        (1, 'Débito'),
        (2, 'Crédito'),
    )

    name = models.CharField('Título do Lançamento:',
                            max_length=255)
    date = models.DateField('Data do Lançamento:',
                            default=datetime.date.today)
    lanc_tp = models.IntegerField('Tipo de Lançamento:',
                                  choices=Transactions_Choices,
                                  default=1)
    value = models.DecimalField('Valor do Lançamento:',
                                max_digits=12,
                                decimal_places=2)
    conta = models.ForeignKey(Conta,
                              related_name='lancamentos',
                              on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User',
                              related_name='lancamentos',
                              on_delete=models.CASCADE)
    objects = LancamentoManager()
