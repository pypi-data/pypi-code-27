"""
Models de Contas
"""
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
