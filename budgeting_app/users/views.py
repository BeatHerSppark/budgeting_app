from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, logout
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.models import PastBudget

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            saved = form.save()
            profile = Profile(user=saved, total=0)
            profile.save()
            login(request, saved)
            request.session["new_user"] = True
            return redirect("app:dashboard")
    else:
        if request.user.is_authenticated:
            return redirect("app:login")
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            prevMonth = datetime.now() - relativedelta(months=1)
            prevMonth = prevMonth.strftime("%Y-%m")
            if prevMonth >= request.user.date_joined.strftime('%Y-%m') and PastBudget.objects.filter(profile=request.user.profile, yyyy_mm=prevMonth).first() is None:
                print("Logging month's budget for ", request.user.username)
                pastBudget = PastBudget(profile=request.user.profile, yyyy_mm=prevMonth, budget_set=request.user.profile.budget)
                pastBudget.save()
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect("app:dashboard")
    else:
        if request.user.is_authenticated:
            return redirect("app:dashboard")
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("users:login")