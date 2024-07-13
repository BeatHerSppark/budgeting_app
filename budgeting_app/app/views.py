from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Transaction, Category
from . import forms

# Create your views here.
@login_required(login_url="/users/login/")
def dashboard_view(request):
    form = forms.AddTransaction()
    expenseCategories = Category.objects.filter(category_type="expense")
    print(expenseCategories)
    incomeCategories = Category.objects.filter(category_type="Income")
    #current_day = datetime.now().strftime('%Y-%m-%d')
    #current_week = datetime.now().strftime('%Y-W%V')
    recent_transactions = Transaction.objects.filter(profile=request.user.profile).order_by("date")[:10]
    return render(request, "app/dashboard.html", {
        "user": request.user,
        "recent_transactions": recent_transactions,
        "form": form,
        "expenseCategories": expenseCategories,
        "incomeCategories": incomeCategories,
    },)

@login_required(login_url="/users/login/")
def transactions_view(request):
    return render(request, "app/transactions.html")

@login_required(login_url="/users/login/")
def categories_view(request):
    return render(request, "app/categories.html")