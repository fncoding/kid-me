from django.db import models
from stocks.models import Product
from django.contrib.auth.models import User

class ShoppingList(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name="owned_shoppinglists", on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through='ShoppingListItem', related_name='shoppinglists')
    shared_with = models.ManyToManyField(User, related_name='shared_shoppinglists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        unique_together = ('shopping_list', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} on {self.shopping_list.name}"

