# Generated by Django 5.0.6 on 2024-09-07 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='currency',
            field=models.CharField(default='USD', max_length=10),
        ),
    ]
