# Generated by Django 5.0.6 on 2024-10-11 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_pastbudget'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pastbudget',
            name='amount_spent',
        ),
    ]
