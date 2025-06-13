from django.urls import path
from . import views

urlpatterns = [
    path('', views.shoppinglist_view, name='shoppinglist'),
    path('edit/<int:item_id>/', views.shoppinglist_edit, name='shoppinglist_edit'),
    path('delete/<int:item_id>/', views.shoppinglist_delete, name='shoppinglist_delete'),
    path('toggle/<int:item_id>/', views.shoppinglist_toggle_purchased, name='shoppinglist_toggle_purchased'),
    path('move_to_inventory/<int:item_id>/', views.shoppinglist_move_to_inventory, name='shoppinglist_move_to_inventory'),
    path('move_all_to_inventory/', views.shoppinglist_move_all_to_inventory, name='shoppinglist_move_all_to_inventory'),
    path('inventory_add/', views.inventory_add, name='inventory_add'),
    path('inventory_edit/<int:item_id>/', views.inventory_edit, name='inventory_edit'),
    path('inventory_delete/<int:item_id>/', views.inventory_delete, name='inventory_delete'),
]