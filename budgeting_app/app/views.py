from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Transaction, Category

# Create your views here.
@login_required(login_url="/users/login/")
def dashboard_view(request):
    request.session.set_expiry(0)
    expenseCategories = Category.objects.filter(category_type="expense")
    incomeCategories = Category.objects.filter(category_type="Income")
    #current_day = datetime.now().strftime('%Y-%m-%d')
    #current_week = datetime.now().strftime('%Y-W%V')
    recent_transactions = Transaction.objects.filter(profile=request.user.profile).order_by("-date")[:10]

    if request.method == "POST":
        transaction_type = request.POST['transaction_type']
        amount = request.POST['amount']
        category = Category.objects.get(title=request.POST['category'])
        date = request.POST['date']
        comment = request.POST['comment']
        profile = request.user.profile

        transaction = Transaction(transaction_type=transaction_type, amount=amount, date=date, profile=profile, category=category, comment=comment)
        transaction.save()
        return redirect("app:dashboard")

    return render(request, "app/dashboard.html", {
        "user": request.user,
        "recent_transactions": recent_transactions,
        "expenseCategories": expenseCategories,
        "incomeCategories": incomeCategories,
    },)

@login_required(login_url="/users/login/")
def transactions_view(request):
    return render(request, "app/transactions.html")

@login_required(login_url="/users/login/")
def categories_view(request):
    defaultExpenseCategories = Category.objects.filter(category_type="expense").filter(default_category="True")
    userExpenseCategories = Category.objects.filter(category_type="expense").filter(profile=request.user.profile)
    defaultIncomeCategories = Category.objects.filter(category_type="income").filter(default_category="True")
    userIncomeCategories = Category.objects.filter(category_type="income").filter(profile=request.user.profile)
    return render(request, "app/categories.html", {
        "defaultExpenseCategories": defaultExpenseCategories,
        "userExpenseCategories": userExpenseCategories,
        "defaultIncomeCategories": defaultIncomeCategories,
        "userIncomeCategories": userIncomeCategories,
    })