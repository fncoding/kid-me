from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ShoppingListItem, InventoryItem

class ShoppingListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_add_shoppinglist_item(self):
        response = self.client.post(reverse('shoppinglist'), {
            'name': 'Milch',
            'quantity': 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ShoppingListItem.objects.filter(user=self.user, name='Milch').exists())

    def test_edit_shoppinglist_item(self):
        item = ShoppingListItem.objects.create(user=self.user, name='Brot', quantity=1)
        response = self.client.post(reverse('shoppinglist_edit', args=[item.id]), {
            'name': 'Vollkornbrot',
            'quantity': 3
        })
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.name, 'Vollkornbrot')
        self.assertEqual(item.quantity, 3)

    def test_delete_shoppinglist_item(self):
        item = ShoppingListItem.objects.create(user=self.user, name='Butter', quantity=1)
        response = self.client.post(reverse('shoppinglist_delete', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ShoppingListItem.objects.filter(id=item.id).exists())

    def test_toggle_purchased(self):
        item = ShoppingListItem.objects.create(user=self.user, name='Käse', quantity=1, purchased=False)
        response = self.client.post(reverse('shoppinglist_toggle_purchased', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertTrue(item.purchased)

    def test_move_to_inventory(self):
        item = ShoppingListItem.objects.create(user=self.user, name='Eier', quantity=5)
        response = self.client.post(reverse('shoppinglist_move_to_inventory', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ShoppingListItem.objects.filter(id=item.id).exists())
        self.assertTrue(InventoryItem.objects.filter(user=self.user, name='Eier', quantity=5).exists())

    def test_move_all_to_inventory(self):
        ShoppingListItem.objects.create(user=self.user, name='Apfel', quantity=2)
        ShoppingListItem.objects.create(user=self.user, name='Birne', quantity=3)
        response = self.client.post(reverse('shoppinglist_move_all_to_inventory'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShoppingListItem.objects.filter(user=self.user).count(), 0)
        self.assertEqual(InventoryItem.objects.filter(user=self.user).count(), 2)

    def test_inventory_add(self):
        response = self.client.post(reverse('inventory_add'), {
            'inv_name': 'Mehl',
            'inv_quantity': 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(InventoryItem.objects.filter(user=self.user, name='Mehl', quantity=4).exists())

    def test_inventory_edit(self):
        inv = InventoryItem.objects.create(user=self.user, name='Zucker', quantity=1)
        response = self.client.post(reverse('inventory_edit', args=[inv.id]), {
            'name': 'Rohrzucker',
            'quantity': 7
        })
        self.assertEqual(response.status_code, 302)
        inv.refresh_from_db()
        self.assertEqual(inv.name, 'Rohrzucker')
        self.assertEqual(inv.quantity, 7)

    def test_inventory_delete(self):
        inv = InventoryItem.objects.create(user=self.user, name='Salz', quantity=1)
        response = self.client.post(reverse('inventory_delete', args=[inv.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(InventoryItem.objects.filter(id=inv.id).exists())
