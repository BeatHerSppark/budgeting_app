from django.db import models
from users.models import Profile
from django.utils.timezone import now

# Create your models here.
class Transaction(models.Model):
    transaction_type = models.BooleanField(default=True) # True = expense, False = income
    amount = models.FloatField()
    date = models.DateField(default=now)
    comment = models.TextField(max_length=200)
