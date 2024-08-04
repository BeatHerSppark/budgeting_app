from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from users.models import Profile
import json
from django.http import JsonResponse
from .models import Transaction, Category, Icon

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
        profile = Profile.objects.get(user=request.user)
        data = json.loads(request.body)
        defaultCategories = Category.objects.filter(default_category=True).filter(category_type=data["category_type"]).values('title')
        userCategories = Category.objects.filter(profile=profile).filter(category_type=data["category_type"]).values('title')
        categories_list = list(defaultCategories) + list(userCategories)
        return  JsonResponse({"categories": categories_list}, status=200)


@login_required(login_url="/users/login/")
def dashboard_edit_transaction(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        transaction = Transaction.objects.get(id=request.POST["id"])
        prevAmount = transaction.amount
        transaction.amount = request.POST["amount"]

        if request.POST["category"] == "Choose a category":
            transaction.category = Category.objects.filter(category_type=request.POST["transaction_type"]).get(title="Uncategorized")
        else:
            transaction.category = Category.objects.filter(category_type=request.POST["transaction_type"]).get(title=request.POST["category"])
        transaction.date = request.POST["date"]
        transaction.comment = request.POST["comment"]

        if request.POST["transaction_type"] == "Expense":
            profile.budget += float(prevAmount)
            profile.budget -= float(transaction.amount)
        else:
            profile.budget -= float(prevAmount)
            profile.budget += float(transaction.amount)

        profile.save()
        transaction.save()
        return redirect("app:dashboard")


@login_required(login_url="/users/login/")
def dashboard_view(request):
    request.session.set_expiry(0)
    defaultExpenseCategories = Category.objects.filter(category_type="Expense").filter(default_category="True")
    userExpenseCategories = Category.objects.filter(category_type="Expense").filter(profile=request.user.profile)
    defaultIncomeCategories = Category.objects.filter(category_type="Income").filter(default_category="True")
    userIncomeCategories = Category.objects.filter(category_type="Income").filter(profile=request.user.profile)

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
        if request.POST["category"] == "Choose a category":
            category = Category.objects.filter(category_type=request.POST["transaction_type"]).get(title="Uncategorized")
        else:
            category = Category.objects.filter(category_type=request.POST["transaction_type"]).get(title=request.POST['category'])
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
        "defaultExpenseCategories": defaultExpenseCategories,
        "userExpenseCategories": userExpenseCategories,
        "defaultIncomeCategories": defaultIncomeCategories,
        "userIncomeCategories": userIncomeCategories,
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
    icons = Icon.objects.all()
    return render(request, "app/categories.html", {
        "defaultExpenseCategories": defaultExpenseCategories,
        "userExpenseCategories": userExpenseCategories,
        "defaultIncomeCategories": defaultIncomeCategories,
        "userIncomeCategories": userIncomeCategories,
        "icons": icons,
    })

@login_required(login_url="/users/login/")
def create_category(request):
    if request.method=="POST":
        profile = Profile.objects.get(user=request.user)
        data = json.loads(request.body)
        title = data["title"]
        icon_tag = "lni-question-circle"
        category_type = data["category_type"]
        if data["icon_tag"] != None:
            icon_tag = data["icon_tag"]

        category = Category(category_type=category_type, default_category=False, title=title, icon_tag=icon_tag, profile=profile)
        category.save()
        return redirect("app:categories")


@login_required(login_url="/users/login/")
def edit_category(request):
    if request.method=="POST":
        profile = Profile.objects.get(user=request.user)
        data = json.loads(request.body)
        category = Category.objects.get(id=data["id"])
        category.title = data["title"]
        category.icon_tag = data["icon_tag"]
        category.save()
        return redirect("app:categories")