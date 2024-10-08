from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, logout

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