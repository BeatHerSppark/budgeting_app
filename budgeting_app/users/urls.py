from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout")
]