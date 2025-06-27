from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class StockList(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='owned_stocklists', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='StockItem', related_name='stocklists')
    shared_with = models.ManyToManyField(User, related_name='shared_stocklists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class StockItem(models.Model):
    stock_list = models.ForeignKey(StockList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('stock_list', 'product')

        def __str__(self):
            return f"{self.quantity} x {self.product.name} in {self.stock_list.name}"