from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('transactions/', views.transactions_view, name="transactions"),
    path('categories/', views.categories_view, name="categories"),
]