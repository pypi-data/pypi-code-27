from django import forms

from djmoney_test.models import MyModel
from djmoney.forms.fields import MoneyField


class MyModelForm(forms.ModelForm):

    amount = MoneyField(disabled=True)

    class Meta:
        fields = '__all__'
        model = MyModel
