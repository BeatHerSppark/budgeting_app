# Generated by Django 5.0.6 on 2024-08-05 12:14

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_transaction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_type',
            field=models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income'), ('Uncategorized', 'Uncategorized')], max_length=13),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(default=None, on_delete=models.SET(app.models.on_delete_category), to='app.category'),
        ),
    ]
