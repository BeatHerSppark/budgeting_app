# Generated by Django 5.0.6 on 2024-08-18 00:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_category_category_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
