from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta, time
from dateutil.relativedelta import relativedelta
from users.models import Profile
import json
import calendar
from collections import defaultdict
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
        transaction.date = request.POST['date']
        transaction.comment = request.POST["comment"]

        if request.POST["transaction_type"] == "Expense":
            profile.total += float(prevAmount)
            profile.total -= float(transaction.amount)
        else:
            profile.total -= float(prevAmount)
            profile.total += float(transaction.amount)

        profile.save()
        transaction.save()
        return redirect("app:" + request.POST['path'])

def handleDashboardLastPeriod(request, selected_date, oldest=False):
    lastExpenseSelection = None
    lastIncomeSelection = None
    start = None
    end = None
    if oldest:
        oldest_transaction = None
        try:
            oldest_transaction = Transaction.objects.earliest("date")
        except Transaction.DoesNotExist:
            oldest_transaction = None
        start = datetime.combine(oldest_transaction.date, time(0, 0, 0)) if oldest_transaction else None

    if selected_date == "today":
        start = (datetime.now() - timedelta(days=1)).date() if start==None else start
        end = (datetime.now() - timedelta(days=1)).date()
        start = datetime.combine(start, time(0, 0, 0))
        end = datetime.combine(end, time(23, 59, 59, 999999))
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    elif selected_date == "week":
        today = datetime.now().date()
        days_to_monday = today.weekday() + 7
        start = today - timedelta(days=days_to_monday) if start==None else start
        end = (today - timedelta(days=today.weekday())) - timedelta(days=1)
        start = datetime.combine(start, time(0, 0, 0))
        end = datetime.combine(end, time(23, 59, 59, 999999))
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    elif selected_date == "month":
        today = datetime.now().date()
        first_of_current_month = today.replace(day=1)
        end = first_of_current_month - timedelta(days=1)
        start = end.replace(day=1) if start==None else start
        start = datetime.combine(start, time(0, 0, 0))
        end = datetime.combine(end, time(23, 59, 59, 999999))
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    else:
        today = datetime.now().date()
        first_of_current_year = today.replace(month=1, day=1)
        end = first_of_current_year - timedelta(days=1)
        start = end.replace(month=1, day=1) if start==None else start
        start = datetime.combine(start, time(0, 0, 0))
        end = datetime.combine(end, time(23, 59, 59, 999999))
        lastExpenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
        lastIncomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))

    return lastExpenseSelection, lastIncomeSelection

@login_required(login_url="/users/login/")
def dashboard_get_chart(request):
    if request.method == "POST":
        start = request.session.get("start")
        end = request.session.get("end")
        selected_date = request.session.get("selected_date")
        categories = []
        expenses = []
        income = []
        if selected_date == "today":
            categories = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M")

            for i in range(24):
                end = start + timedelta(minutes=59, seconds=59)
                expensesSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
                incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))

                expenseSum=0
                incomeSum=0

                for exp in expensesSelection:
                    expenseSum += exp.amount

                for inc in incomeSelection:
                    incomeSum += inc.amount

                expenses.append(expenseSum)
                income.append(incomeSum)


                start = start + timedelta(hours=1)

        if selected_date == "week":
            today = datetime.today()
            monday = today - timedelta(days=today.weekday())

            categories = [
                (monday + timedelta(days=day)).strftime("%A")
                for day in range((today - monday).days + 1)
            ]
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M")

            for i in range(len(categories)):
                end = start + timedelta(hours=23, minutes=59, seconds=59)
                expensesSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
                incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
                expenseSum=0
                incomeSum=0

                for exp in expensesSelection:
                    expenseSum += exp.amount

                for inc in incomeSelection:
                    incomeSum += inc.amount

                expenses.append(expenseSum)
                income.append(incomeSum)

                start = start + timedelta(days=1)

        if selected_date == "month":
            today = datetime.today()
            current_day = today.day

            categories = [f"{day:02}" for day in range(1, current_day + 1)]
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M")

            for i in range(current_day):
                end = start + timedelta(hours=23, minutes=59, seconds=59)
                expensesSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
                incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
                expenseSum=0
                incomeSum=0

                for exp in expensesSelection:
                    expenseSum += exp.amount

                for inc in incomeSelection:
                    incomeSum += inc.amount

                expenses.append(expenseSum)
                income.append(incomeSum)

                start = start + timedelta(days=1)

        if selected_date == "year":
            today = datetime.today()
            current_year = today.year
            current_month = today.month
            categories = [
                datetime(current_year, month, 1).strftime("%B")
                for month in range(1, current_month + 1)
]
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M")

            for month in range(1, len(categories)+1):
                last_day = calendar.monthrange(current_year, month)[1]
                end = datetime(current_year, month, last_day, 23, 59)

                expensesSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
                incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
                expenseSum=0
                incomeSum=0

                for exp in expensesSelection:
                    expenseSum += exp.amount

                for inc in incomeSelection:
                    incomeSum += inc.amount

                expenses.append(expenseSum)
                income.append(incomeSum)

                start = start + relativedelta(months=1)

        return JsonResponse({"categories": categories, "expenses": expenses, "income": income})

@login_required(login_url="/users/login/")
def set_date_range(request):
    if request.method == "POST":
        data = json.loads(request.body)
        start = data["start"]
        end = data["end"]
        selected_date = data["selected_date"]
        if start==None or end==None:
            end = date.today()
            start = end - timedelta(days=end.weekday())
            selected_date = "week"
        else:
            start = datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.strptime(end, "%Y-%m-%d").date()
        start = datetime.combine(start, time(0, 0, 0))
        end = datetime.combine(end, time(23, 59, 59, 999999))

        request.session["start"] = start.strftime('%Y-%m-%dT%H:%M')
        request.session["end"] = end.strftime('%Y-%m-%dT%H:%M')
        request.session["selected_date"] = selected_date

        return JsonResponse({"start": start, "end": end, "selected_date": selected_date})


@login_required(login_url="/users/login/")
def dashboard_view(request):
    request.session.set_expiry(0)
    defaultExpenseCategories = Category.objects.filter(category_type="Expense").filter(default_category="True")
    userExpenseCategories = Category.objects.filter(category_type="Expense").filter(profile=request.user.profile)
    defaultIncomeCategories = Category.objects.filter(category_type="Income").filter(default_category="True")
    userIncomeCategories = Category.objects.filter(category_type="Income").filter(profile=request.user.profile)

    current_day = datetime.now().strftime('%Y-%m-%dT%H:%M')
    #current_week = datetime.now().strftime('%Y-W%V')
    recent_transactions = Transaction.objects.filter(profile=request.user.profile).order_by("-submission_time")[:10]

    start = request.session.get("start")
    end = request.session.get("end")
    selected_date = request.session.get("selected_date")
    if start==None or end==None or selected_date=="allTime":
        end = date.today()
        start = end - timedelta(days=end.weekday())
        selected_date = "week"
        start = datetime.combine(start, time(0, 0, 0))
        end = datetime.combine(end, time(23, 59, 59, 999999))
        request.session["start"] = start.strftime('%Y-%m-%dT%H:%M')
        request.session["end"] = end.strftime('%Y-%m-%dT%H:%M')
        request.session["selected_date"] = selected_date

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

    if request.method == "POST":
        transaction_type = request.POST['transaction_type']
        amount = request.POST['amount']
        if(float(amount) < 0):
            messages.error(request, "Amount can't be negative.")
            return redirect(request.path_info)
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

        return redirect(request.path_info)

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
        if(float(data["budget"]) < 0):
            messages.error(request, "Budget can't be negative.")
            return JsonResponse({"message": "Budget can't be negative."}, status=200)
        profile = Profile.objects.get(user=request.user)
        profile.budget = data["budget"]
        profile.save()
        return JsonResponse({"message": "Changed budget successfully."}, status=200)

@login_required(login_url="/users/login/")
def get_budget(request):
    today = datetime.today()
    beginning_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = None
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        next_month = today.replace(month=today.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

    end_of_month = next_month - timedelta(seconds=1)
    transactions = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(beginning_of_month, end_of_month))
    spent_this_month = 0
    for transaction in transactions:
        spent_this_month += transaction.amount

    percentSpent = round((spent_this_month / request.user.profile.budget)*100, 2) if request.user.profile.budget!=0 else 0

    days_left = (next_month - today).days +1 if (next_month - today).days!=0 else 1
    remaining_budget = request.user.profile.budget - spent_this_month
    daily_spending = round(remaining_budget / days_left, 2)

    return JsonResponse({"spent_this_month": spent_this_month, "percent_spent": percentSpent, "daily_spending": daily_spending, "days_left": days_left}, status=200)

@login_required(login_url="/users/login/")
def get_pie_chart(request):
    if request.method == "POST":
        start = request.session.get("start")
        end = request.session.get("end")
        defaultExpenseCategories = Category.objects.filter(category_type="Expense").filter(default_category="True")
        userExpenseCategories = Category.objects.filter(category_type="Expense").filter(profile=request.user.profile)
        defaultIncomeCategories = Category.objects.filter(category_type="Income").filter(default_category="True")
        userIncomeCategories = Category.objects.filter(category_type="Income").filter(profile=request.user.profile)
        expenseCategoriesDict = defaultdict(int)
        incomeCategoriesDict = defaultdict(int)
        totalExp = 0
        totalInc = 0

        for category in defaultExpenseCategories:
            exp = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end)).filter(category=category)
            for el in exp:
                expenseCategoriesDict[el.category.title] += 1
                totalExp += 1
        for category in userExpenseCategories:
            exp = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end)).filter(category=category)
            for el in exp:
                expenseCategoriesDict[el.category.title] += 1
                totalExp += 1
        for el in Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end)).filter(category=Category.objects.get(title="Uncategorized")):
            expenseCategoriesDict[el.category.title] += 1
            totalExp += 1
        for category in defaultIncomeCategories:
            exp = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end)).filter(category=category)
            for el in exp:
                incomeCategoriesDict[el.category.title] += 1
                totalInc += 1
        for category in userIncomeCategories:
            exp = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end)).filter(category=category)
            for el in exp:
                incomeCategoriesDict[el.category.title] += 1
                totalInc += 1
        for el in Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end)).filter(category=Category.objects.get(title="Uncategorized")):
            incomeCategoriesDict[el.category.title] += 1
            totalInc += 1

        for key in expenseCategoriesDict:
            expenseCategoriesDict[key] = (expenseCategoriesDict[key]/totalExp)*100
        for key in incomeCategoriesDict:
            incomeCategoriesDict[key] = (incomeCategoriesDict[key]/totalInc)*100

        return JsonResponse({"expenseCategories": expenseCategoriesDict, "incomeCategories": incomeCategoriesDict})

@login_required(login_url="/users/login/")
def set_sort_date(request):
    if request.method == "POST":
        if request.session.get("sortTransactions") == "-date":
            request.session["sortTransactions"] = "date"
        else:
            request.session["sortTransactions"] = "-date"
        return JsonResponse({"message": "working"}, status=200)

@login_required(login_url="/users/login/")
def set_sort_amount(request):
    if request.method == "POST":
        if request.session.get("sortTransactions") == "-amount":
                request.session["sortTransactions"] = "amount"
        else:
            request.session["sortTransactions"] = "-amount"
        return JsonResponse({"message": "working"}, status=200)

@login_required(login_url="/users/login/")
def search_transactions(request):
    if request.method == "POST":
        start = request.session.get("start")
        end = request.session.get("end")
        data = json.loads(request.body)
        search_text = data["searchText"]
        transactions = Transaction.objects.filter(
            profile=request.user.profile, date__range=(start, end), amount__istartswith=search_text) | Transaction.objects.filter(
            profile=request.user.profile, date__range=(start, end), date__icontains=search_text) | Transaction.objects.filter(
            profile=request.user.profile, date__range=(start, end), transaction_type__icontains=search_text) | Transaction.objects.filter(
            profile=request.user.profile, date__range=(start, end), category__title__icontains=search_text) | Transaction.objects.filter(
            profile=request.user.profile, date__range=(start, end), comment__icontains=search_text)

        transactions = transactions.order_by(request.session.get("sortTransactions"))
        print(transactions)
        listTransactions = list(transactions.values("id", "category__title", "amount", "comment", "date", "profile", "transaction_type"))
        return JsonResponse({"search_transactions": listTransactions}, status=200)

@login_required(login_url="/users/login/")
def transactions_view(request):
    current_day = datetime.now().strftime('%Y-%m-%dT%H:%M')
    start = request.session.get("start")
    end = request.session.get("end")
    selected_date = request.session.get("selected_date")
    if start==None or end==None:
        end = date.today()
        start = end - timedelta(days=end.weekday())
        selected_date = "week"
        start = datetime.combine(start, time(0, 0, 0))
        end = datetime.combine(end, time(23, 59, 59, 999999))

    if not request.session.has_key("sortTransactions"):
        request.session["sortTransactions"] = "-date"

    transactions = Transaction.objects.filter(profile=request.user.profile).filter(date__range=(start, end)).order_by(request.session.get("sortTransactions"))
    paginator = Paginator(transactions, 15)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    expenseSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Expense").filter(date__range=(start, end))
    incomeSelection = Transaction.objects.filter(profile=request.user.profile).filter(transaction_type="Income").filter(date__range=(start, end))
    expenses = 0
    income = 0
    for expense in expenseSelection:
        expenses += expense.amount
    for earning in incomeSelection:
        income += earning.amount

    percentProductivity = round(((income-expenses)/income)*100, 2) if income!=0 else 0

    defaultExpenseCategories = Category.objects.filter(category_type="Expense").filter(default_category="True")
    userExpenseCategories = Category.objects.filter(category_type="Expense").filter(profile=request.user.profile)
    defaultIncomeCategories = Category.objects.filter(category_type="Income").filter(default_category="True")
    userIncomeCategories = Category.objects.filter(category_type="Income").filter(profile=request.user.profile)

    if request.method == "POST":
        transaction_type = request.POST['transaction_type']
        amount = request.POST['amount']
        if(float(amount) < 0):
            messages.error(request, "Amount can't be negative.")
            return redirect(request.path_info)
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

        return redirect(request.path_info)

    return render(request, "app/transactions.html", {
        "transactions": transactions,
        "page_obj": page_obj,
        "selected_date": selected_date,
        "expenses": expenses,
        "income": income,
        "percentProductivity": percentProductivity,
        "defaultExpenseCategories": defaultExpenseCategories,
        "userExpenseCategories": userExpenseCategories,
        "defaultIncomeCategories": defaultIncomeCategories,
        "userIncomeCategories": userIncomeCategories,
        "current_day": current_day,
        "sortTransactions": request.session.get('sortTransactions'),
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