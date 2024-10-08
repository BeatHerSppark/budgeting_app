# Generated by Django 5.0.6 on 2024-07-07 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('expense', 'Expense'), ('income', 'Income')], max_length=7),
        ),
    ]
