from django.db import models
from users.models import Profile
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    CHOICES = [
        ('Expense', 'Expense'),
        ('Income', 'Income')
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
        ('Expense', 'Expense'),
        ('Income', 'Income')
    ]
    transaction_type = models.CharField(max_length=7, choices=CHOICES)
    amount = models.FloatField()
    date = models.DateField(default=now)
    submission_time = models.DateTimeField(default=now)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, default=None)
    comment = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.amount) + " " + self.profile.user.username


class Icon(models.Model):
    icon_tag = models.CharField(max_length=50)

    def __str__(self):
        return self.icon_tag