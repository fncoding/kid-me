from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDeleteView, ProductEditView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('new/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
]