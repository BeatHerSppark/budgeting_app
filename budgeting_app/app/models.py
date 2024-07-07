from django.db import models
from users.models import Profile
from django.utils.timezone import now

# Create your models here.
class Transaction(models.Model):
    CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income')
    ]
    transaction_type = models.CharField(max_length=7, choices=CHOICES)
    amount = models.FloatField()
    date = models.DateField(default=now)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, default=None)
    comment = models.TextField(max_length=200, blank=True, null=True)
