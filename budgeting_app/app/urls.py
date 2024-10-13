from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'app'

urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('dashboard-delete-transactions', csrf_exempt(views.dashboard_delete_transactions), name="dashboard_delete_transactions"),
    path('dashboard-get-categories', csrf_exempt(views.dashboard_get_categories), name="dashboard_get_categories"),
    path('dashboard-edit-transaction', views.dashboard_edit_transaction, name="dashboard_edit_transaction"),
    path('dashboard-get-chart', csrf_exempt(views.dashboard_get_chart), name="dashboard_get_chart"),
    path('transactions/', views.transactions_view, name="transactions"),
    path('categories/', views.categories_view, name="categories"),
    path('summaries/', views.summaries_view, name="summaries"),
    path('create-category', csrf_exempt(views.create_category), name="create_category"),
    path('edit-category', csrf_exempt(views.edit_category), name="edit_category"),
    path('delete-category', csrf_exempt(views.delete_category), name="delete_category"),
    path('edit-budget', csrf_exempt(views.edit_budget), name="edit_budget"),
    path('get-budget', csrf_exempt(views.get_budget), name="get_budget"),
    path('set-date-range', csrf_exempt(views.set_date_range), name="set_date_range"),
    path('get-pie-chart', csrf_exempt(views.get_pie_chart), name="get_pie_chart"),
    path('set-sort-date', csrf_exempt(views.set_sort_date), name="set_sort_date"),
    path('set-sort-amount', csrf_exempt(views.set_sort_amount), name="set_sort_amount"),
    path('search-transactions', csrf_exempt(views.search_transactions), name="search_transactions"),
    path('get-expenses', csrf_exempt(views.get_expenses), name="get_expenses"),
    path('settings', views.settings_view, name="settings"),
    path('get-rates', csrf_exempt(views.get_rates), name="get_rates"),
    path('change-pfp', csrf_exempt(views.change_pfp), name="change_pfp"),
    path('delete_user', views.delete_user, name="delete_user"),
    path('export-csv', views.export_csv, name="export_csv"),
]