from django import forms
from . import models

class AddTransaction(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['amount', 'transaction_type', 'category', 'date', 'comment']