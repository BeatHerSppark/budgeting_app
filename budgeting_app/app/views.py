from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/users/login/")
def dashboard_view(request):
    return render(request, "app/dashboard.html")

@login_required(login_url="/users/login/")
def transactions_view(request):
    return render(request, "app/transactions.html")

@login_required(login_url="/users/login/")
def categories_view(request):
    return render(request, "app/categories.html")