from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'app'

urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('dashboard-delete-transactions', csrf_exempt(views.dashboard_delete_transactions), name="dashboard_delete_transactions"),
    path('dashboard-get-categories', csrf_exempt(views.dashboard_get_categories), name="dashboard_get_categories"),
    path('dashboard-edit-transaction', views.dashboard_edit_transaction, name="dashboard_edit_transaction"),
    path('transactions/', views.transactions_view, name="transactions"),
    path('categories/', views.categories_view, name="categories"),
    path('create-category', csrf_exempt(views.create_category), name="create_category"),
    path('edit-category', csrf_exempt(views.edit_category), name="edit_category"),
]