from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShoppingListItem, InventoryItem

@login_required
def shoppinglist_view(request):
    items = ShoppingListItem.objects.filter(user=request.user)
    inventory = InventoryItem.objects.filter(user=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = int(request.POST.get("quantity", 1))
        if name:
            ShoppingListItem.objects.create(user=request.user, name=name, quantity=quantity)
            return redirect('shoppinglist')
    return render(request, "shoppinglist/shoppinglist.html", {
        "items": items,
        "inventory": inventory,
    })

@login_required
def shoppinglist_edit(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    if request.method == "POST":
        item.name = request.POST.get("name", item.name)
        item.quantity = int(request.POST.get("quantity", item.quantity))
        item.save()
        return redirect('shoppinglist')
    return render(request, "shoppinglist/shoppinglist_edit.html", {"item": item})

@login_required
def shoppinglist_delete(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect('shoppinglist')
    return render(request, "shoppinglist/shoppinglist_delete.html", {"item": item})

@login_required
def shoppinglist_toggle_purchased(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    item.purchased = not item.purchased
    item.save()
    return redirect('shoppinglist')

@login_required
def shoppinglist_move_to_inventory(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    if request.method == "POST":
        inv, created = InventoryItem.objects.get_or_create(user=request.user, name=item.name)
        inv.quantity += item.quantity
        inv.save()
        item.delete()
    return redirect('shoppinglist')

@login_required
def shoppinglist_move_all_to_inventory(request):
    if request.method == "POST":
        items = ShoppingListItem.objects.filter(user=request.user)
        for item in items:
            inv, created = InventoryItem.objects.get_or_create(user=request.user, name=item.name)
            inv.quantity += item.quantity
            inv.save()
            item.delete()
    return redirect('shoppinglist')

@login_required
def inventory_add(request):
    if request.method == "POST":
        name = request.POST.get("inv_name")
        quantity = int(request.POST.get("inv_quantity", 1))
        if name:
            inv, created = InventoryItem.objects.get_or_create(user=request.user, name=name)
            inv.quantity += quantity
            inv.save()
        return redirect('shoppinglist')
    
@login_required
def inventory_edit(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id, user=request.user)
    if request.method == "POST":
        item.name = request.POST.get("name", item.name)
        item.quantity = int(request.POST.get("quantity", item.quantity))
        item.save()
        return redirect('shoppinglist')
    return render(request, "shoppinglist/inventory_edit.html", {"item": item})

@login_required
def inventory_delete(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect('shoppinglist')
    return render(request, "shoppinglist/inventory_delete.html", {"item": item})
