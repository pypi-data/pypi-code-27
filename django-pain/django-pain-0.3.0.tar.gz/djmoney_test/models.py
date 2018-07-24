from django.db import models
from djmoney.models.fields import MoneyField


class MyModel(models.Model):
    amount = MoneyField(max_digits=64, decimal_places=4)
