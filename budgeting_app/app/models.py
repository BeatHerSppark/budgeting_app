from django.db import models

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('earning', 'Earning'),
    ]

    sum_of_money = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    date_of_transaction = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.sum_of_money} on {self.date_of_transaction}"