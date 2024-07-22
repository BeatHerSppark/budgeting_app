from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'app'

urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('dashboard-delete-transactions', csrf_exempt(views.dashboard_delete_transactions), name="dashboard_delete_transactions"),
    path('transactions/', views.transactions_view, name="transactions"),
    path('categories/', views.categories_view, name="categories"),
]