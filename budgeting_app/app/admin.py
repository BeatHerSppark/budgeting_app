from django.contrib import admin
from .models import Transaction, Category, Icon, PastBudget

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Icon)
admin.site.register(PastBudget)