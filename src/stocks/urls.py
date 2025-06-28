from django.urls import path
from .views import StockListView, StockListCreateView, StockListUpdateView, StockListDeleteView, StockListView, StockListDetailView, StockListItemView, StockListItemCreateView, StockListItemUpdateView, StockListItemDeleteView, toggle_item_purchased, update_item_fields

urlpatterns = [
    path('', StockListView.as_view(), name='stocklists'),
    path('new/', StockListCreateView.as_view(), name='stocklist_create'),
    path('<int:pk>/', StockListDetailView.as_view(), name='stocklist_detail'),
    path('<int:pk>/edit/', StockListUpdateView.as_view(), name='stocklist_update'),
    path('<int:pk>/delete/', StockListDeleteView.as_view(), name='stocklist_delete'),
    path('<int:pk>/items/', StockListItemView.as_view(), name='stocklist_items'),
    path('<int:pk>/items/new/', StockListItemCreateView.as_view(), name='stocklist_item_create'),
    path('<int:pk>/items/<int:item_pk>/edit/', StockListItemUpdateView.as_view(), name='stocklist_item_update'),
    path('<int:pk>/items/<int:item_pk>/delete/', StockListItemDeleteView.as_view(), name='stocklist_item_delete'),
    path('<int:pk>/items/<int:item_pk>/toggle/', toggle_item_purchased, name='stocklist_item_toggle'),
    path('<int:pk>/items/<int:item_pk>/update/', update_item_fields, name='stocklist_item_update_fields'),
]
