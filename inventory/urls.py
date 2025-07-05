from django.urls import path
from . import views
from .views import add_stock_entry, InventoryDashboardView , search_entries_api,  delete_entries_api,  entry_edit_api



urlpatterns = [
    path('add/', views.add_stock_entry, name='add_stock_entry'),
    path('', InventoryDashboardView.as_view(), name='inventory_dashboard'),
    path('add/', add_stock_entry, name='add_stock_entry'),  
    path('api/search/', search_entries_api, name='search_api'),
    path('api/delete/', delete_entries_api, name='delete_api'),
    path('api/entry/<int:pk>/', entry_edit_api, name='entry_edit_api'),
]