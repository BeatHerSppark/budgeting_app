from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from users.models import Profile
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
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
                profile.total += float(transaction.amount)
            else:
                profile.total -= float(transaction.amount)
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
            transaction.category = Category.objects.get(category_type="Uncategorized")
        else:
            transaction.category = Category.objects.filter(category_type=request.POST["transaction_type"]).get(title=request.POST["category"])
        transaction.date = request.POST["date"]
        transaction.comment = request.POST["comment"]

        if request.POST["transaction_type"] == "Expense":
            profile.total += float(prevAmount)
            profile.total -= float(transaction.amount)
        else:
            profile.total -= float(prevAmount)
            profile.total += float(transaction.amount)

        profile.save()
        transaction.save()
        return redirect("app:dashboard")

def handleDashboardLastPeriod(request, selected_date, oldest=False):
    lastExpenseSelection = None
    lastIncomeSelection = None
    start = None
    end = None
    if oldest:
        oldest_transaction = Transaction.objects.earliest("date")
        start = oldest_transaction.date

    if selected_date == "today":
        start = (datetime.now() - timedelta(days=1)).date() if start==None else start
        end = (datetime.now() - timedelta(days=1)).date()
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    elif selected_date == "week":
        today = datetime.now().date()
        days_to_monday = today.weekday() + 7
        start = today - timedelta(days=days_to_monday) if start==None else start
        end = start + timedelta(days=6)
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    elif selected_date == "month":
        today = datetime.now().date()
        first_of_current_month = today.replace(day=1)
        end = first_of_current_month - timedelta(days=1)
        start = end.replace(day=1) if start==None else start
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    else:
        today = datetime.now().date()
        first_of_current_year = today.replace(month=1, day=1)
        end = first_of_current_year - timedelta(days=1)
        start = end.replace(month=1, day=1) if start==None else start
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))

    return lastExpenseSelection, lastIncomeSelection

@login_required(login_url="/users/login/")
def dashboard_get_chart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        expenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(data['start'], data['end']))
        incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(data['start'], data['end']))

        return JsonResponse({"data": data})

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

    start = request.GET.get("start")
    end = request.GET.get("end")
    selected_date = request.GET.get("selected_date")
    if start==None or end==None:
        end = date.today()
        start = end - timedelta(days=end.weekday())
        selected_date = "week"

    expenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
    incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    expenses = 0
    income = 0
    for expense in expenseSelection:
        expenses += expense.amount
    for earning in incomeSelection:
        income += earning.amount

    lastExpenseSelection, lastIncomeSelection = handleDashboardLastPeriod(request, selected_date)
    lastExpenses = 0
    lastIncome = 0
    for expense in lastExpenseSelection:
        lastExpenses += expense.amount
    for earning in lastIncomeSelection:
        lastIncome += earning.amount

    percentExpenses = round(((expenses - lastExpenses)/lastExpenses)*100, 2) if lastExpenses!=0 else 0
    percentIncome = round(((income - lastIncome)/lastIncome)*100, 2) if lastIncome!=0 else 0
    if expenses == 0:
        percentExpenses = 0
    if income == 0:
        percentIncome = 0

    totalExpenseSelection, totalIncomeSelection = handleDashboardLastPeriod(request, selected_date, True)
    totalExpenses = 0
    totalIncome = 0
    for expense in totalExpenseSelection:
        totalExpenses += expense.amount
    for earning in totalIncomeSelection:
        totalIncome += earning.amount

    lastTotal = totalIncome - totalExpenses
    percentTotal = round(((request.user.profile.total - lastTotal)/abs(lastTotal))*100, 2) if lastTotal!=0 else 0
    print(percentTotal)

    if request.method == "POST":
        transaction_type = request.POST['transaction_type']
        amount = request.POST['amount']
        if request.POST["category"] == "Choose a category":
            category = Category.objects.get(category_type="Uncategorized")
        else:
            category = Category.objects.filter(category_type=request.POST["transaction_type"]).get(title=request.POST['category'])
        dateTransaction = request.POST['date']
        comment = request.POST['comment']

        profile = Profile.objects.get(user=request.user)
        if transaction_type == "Expense":
            profile.total -= float(amount)
        else:
            profile.total += float(amount)
        profile.save()
        transaction = Transaction(transaction_type=transaction_type, amount=amount, date=dateTransaction, profile=profile, category=category, comment=comment)
        transaction.save()

        post_start = request.POST['start'] if request.POST['start']!="0" else start
        post_end = request.POST['end'] if request.POST['end']!="0" else end
        post_selected_date = request.POST['selected_date'] if request.POST['selected_date']!="0" else selected_date

        url = f"{request.path_info}?start={post_start}&end={post_end}&selected_date={post_selected_date}"

        return redirect(url) if request.POST['start'] else redirect(request.path_info)

    return render(request, "app/dashboard.html", {
        "current_day": current_day,
        "recent_transactions": recent_transactions,
        "defaultExpenseCategories": defaultExpenseCategories,
        "userExpenseCategories": userExpenseCategories,
        "defaultIncomeCategories": defaultIncomeCategories,
        "userIncomeCategories": userIncomeCategories,
        "expenses": expenses,
        "income": income,
        "selected_date": selected_date,
        "lastExpenses": lastExpenses,
        "lastIncome": lastIncome,
        "lastTotal": lastTotal,
        "percentExpenses": percentExpenses,
        "percentIncome": percentIncome,
        "percentTotal": percentTotal,
    },)

@login_required(login_url="/users/login/")
def edit_budget(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile = Profile.objects.get(user=request.user)
        profile.budget = data["budget"]
        profile.save()
        return JsonResponse({"message": "Changed budget successfully."}, status=200)


@login_required(login_url="/users/login/")
def transactions_view(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    transactions = None
    selected_date = request.GET.get("date")
    if start==None or end==None:
        end = date.today()
        start = end - timedelta(days=end.weekday())
        transactions = Transaction.objects.filter(profile=request.user.profile).filter(date__range=(start, end)).order_by("-date")
        selected_date = "week"
    else:
        transactions = Transaction.objects.filter(profile=request.user.profile).filter(date__range=(start, end)).order_by("-date")

    expenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
    incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    expenses = 0
    income = 0
    for expense in expenseSelection:
        expenses += expense.amount
    for earning in incomeSelection:
        income += earning.amount

    return render(request, "app/transactions.html", {
        "transactions": transactions,
        "selected_date": selected_date,
        "expenses": expenses,
        "income": income,
    })


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
        if data["icon_tag"]:
            category.icon_tag = data["icon_tag"]
        else:
            category.icon_tag = "lni-question-circle"
        category.save()
        return redirect("app:categories")


@login_required(login_url="/users/login/")
def delete_category(request):
    if request.method=="POST":
        data = json.loads(request.body)
        category = Category.objects.get(id=data["id"])
        category.delete()

        return JsonResponse({'message': "Category deleted successfully."}, status=200)