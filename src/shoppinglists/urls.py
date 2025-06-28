from django.urls import path
from .views import ShoppingListView, ShoppingListCreateView, ShoppingListUpdateView, ShoppingListDeleteView, ShoppingListView, ShoppingListDetailView, ShoppingListItemView, ShoppingListItemCreateView, ShoppingListItemUpdateView, ShoppingListItemDeleteView, toggle_item_purchased, update_item_fields, transfer_shoppinglist_to_stock, product_autocomplete

urlpatterns = [
    path('', ShoppingListView.as_view(), name='shoppinglists'),
    path('new/', ShoppingListCreateView.as_view(), name='shoppinglist_create'),
    path('<int:pk>/', ShoppingListDetailView.as_view(), name='shoppinglist_detail'),
    path('<int:pk>/edit/', ShoppingListUpdateView.as_view(), name='shoppinglist_update'),
    path('<int:pk>/delete/', ShoppingListDeleteView.as_view(), name='shoppinglist_delete'),
    path('<int:pk>/items/', ShoppingListItemView.as_view(), name='shoppinglist_items'),
    path('<int:pk>/items/new/', ShoppingListItemCreateView.as_view(), name='shoppinglist_item_create'),
    path('<int:pk>/items/<int:item_pk>/edit/', ShoppingListItemUpdateView.as_view(), name='shoppinglist_item_update'),
    path('<int:pk>/items/<int:item_pk>/delete/', ShoppingListItemDeleteView.as_view(), name='shoppinglist_item_delete'),
    path('<int:pk>/items/<int:item_pk>/toggle/', toggle_item_purchased, name='shoppinglist_item_toggle'),
    path('<int:pk>/items/<int:item_pk>/update/', update_item_fields, name='shoppinglist_item_update_fields'),
    path('<int:pk>/transfer_to_stock/', transfer_shoppinglist_to_stock, name='shoppinglist_transfer_to_stock'),
    path('product-autocomplete/', product_autocomplete, name='product_autocomplete'),
]
