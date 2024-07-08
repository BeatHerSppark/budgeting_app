from django.db import models
from users.models import Profile
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income')
    ]
    category_type = models.CharField(max_length=7, choices=CHOICES)
    default_category = models.BooleanField(default=False) # Premade categories have value True, user-made categories have value False
    title = models.CharField(max_length=50)
    icon_tag = models.CharField(max_length=50)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income')
    ]
    transaction_type = models.CharField(max_length=7, choices=CHOICES)
    amount = models.FloatField()
    date = models.DateField(default=now)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, default=None)
    comment = models.TextField(max_length=200, blank=True, null=True)


class Icon(models.Model):
    icon_tag = models.CharField(max_length=50)
    category = models.CharField(max_length=50)