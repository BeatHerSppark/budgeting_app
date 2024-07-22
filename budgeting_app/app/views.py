from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from users.models import Profile
import json
from django.http import JsonResponse
from .models import Transaction, Category

# Create your views here.
@login_required(login_url="/users/login/")
def dashboard_delete_transactions(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile = Profile.objects.get(user=request.user)

        for transactionID in data['checkedIDs']:
            transaction = Transaction.objects.get(id=int(transactionID))
            if transaction.transaction_type == "Expense":
                profile.budget += float(transaction.amount)
            else:
                profile.budget -= float(transaction.amount)
            profile.save()
            transaction.delete()

        return JsonResponse({'message': "Transactions deleted successfully."}, status=200)


@login_required(login_url="/users/login/")
def dashboard_get_categories(request):
    if request.method == "POST":
        data = json.loads(request.body)
        categories = Category.objects.filter(category_type=data["category_type"]).values('title')
        categories_list = list(categories)
        return  JsonResponse({"categories": categories_list}, status=200)


@login_required(login_url="/users/login/")
def dashboard_view(request):
    request.session.set_expiry(0)
    expenseCategories = Category.objects.filter(category_type="Expense")
    incomeCategories = Category.objects.filter(category_type="Income")
    categories = Category.objects.all()
    current_day = datetime.now().strftime('%Y-%m-%d')
    #current_week = datetime.now().strftime('%Y-W%V')
    recent_transactions = Transaction.objects.filter(profile=request.user.profile).order_by("-submission_time")[:10]
    userExpenseTransactions = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense")
    userIncomeTransactions = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income")
    expenses = 0
    income = 0
    for expense in userExpenseTransactions:
        expenses += expense.amount
    for earning in userIncomeTransactions:
        income += earning.amount

    if request.method == "POST":
        transaction_type = request.POST['transaction_type']
        amount = request.POST['amount']
        category = Category.objects.get(title=request.POST['category'])
        date = request.POST['date']
        comment = request.POST['comment']

        profile = Profile.objects.get(user=request.user)
        if transaction_type == "Expense":
            profile.budget -= float(amount)
        else:
            profile.budget += float(amount)
        profile.save()

        transaction = Transaction(transaction_type=transaction_type, amount=amount, date=date, profile=profile, category=category, comment=comment)
        transaction.save()
        return redirect("app:dashboard")

    return render(request, "app/dashboard.html", {
        "current_day": current_day,
        "recent_transactions": recent_transactions,
        "expenseCategories": expenseCategories,
        "incomeCategories": incomeCategories,
        "categories": categories,
        "expenses": expenses,
        "income": income,
    },)

@login_required(login_url="/users/login/")
def transactions_view(request):
    return render(request, "app/transactions.html")

@login_required(login_url="/users/login/")
def categories_view(request):
    defaultExpenseCategories = Category.objects.filter(category_type="Expense").filter(default_category="True")
    userExpenseCategories = Category.objects.filter(category_type="Expense").filter(profile=request.user.profile)
    defaultIncomeCategories = Category.objects.filter(category_type="Income").filter(default_category="True")
    userIncomeCategories = Category.objects.filter(category_type="Income").filter(profile=request.user.profile)
    return render(request, "app/categories.html", {
        "defaultExpenseCategories": defaultExpenseCategories,
        "userExpenseCategories": userExpenseCategories,
        "defaultIncomeCategories": defaultIncomeCategories,
        "userIncomeCategories": userIncomeCategories,
    })