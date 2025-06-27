from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import ShoppingList, ShoppingListItem
from .forms import ShoppingListForm, ShoppingListUpdateForm, ShoppingListItemForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


# ShoppingListView: List all shopping lists for the logged-in user, including those shared with them.
class ShoppingListView(LoginRequiredMixin, ListView):
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shoppinglist.html'
    context_object_name = 'shoppinglists'
    
    # Ensure the user is logged in before accessing this view
    def get_queryset(self):
        return ShoppingList.objects.filter(Q(owner=self.request.user) | Q(shared_with=self.request.user)).distinct()


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shoppinglist_create.html'
    success_url = reverse_lazy('shoppinglists')
    

class ShoppingListDeleteView(DeleteView):
    model = ShoppingList
    success_url = reverse_lazy('shoppinglists')

class ShoppingListUpdateView(UpdateView):
    model = ShoppingList
    form_class = ShoppingListUpdateForm
    template_name = 'shoppinglist_update.html'
    success_url = reverse_lazy('shoppinglists')

class ShoppingListDetailView(LoginRequiredMixin, DetailView):
    model = ShoppingList
    template_name = 'shoppinglist_detail.html'
    context_object_name = 'shoppinglist'

# ShoppingListItemView: List all items in a shopping list, allowing the user to add new items.
class ShoppingListItemView(LoginRequiredMixin, ListView):
    model = ShoppingListItem
    template_name = 'shoppinglist_item/shoppinglist_item.html'
    context_object_name = 'shoppinglist_items'

    def get_queryset(self):
        self.shoppinglist = ShoppingList.objects.get(pk=self.kwargs['pk'])
        return ShoppingListItem.objects.filter(shopping_list=self.shoppinglist)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoppinglist'] = ShoppingList.objects.get(pk=self.kwargs['pk'])
        return context

  
class ShoppingListItemCreateView(CreateView):
    model = ShoppingListItem
    form_class = ShoppingListItemForm
    template_name = 'shoppinglist_item/shoppinglist_item_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoppinglist'] = ShoppingList.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.shopping_list = ShoppingList.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shoppinglist_items', kwargs={'pk': self.kwargs['pk']})

class ShoppingListItemUpdateView(UpdateView):
    model = ShoppingListItem
    form_class = ShoppingListItemForm
    template_name = 'shoppinglist_item/shoppinglist_item_update.html'

    def get_object(self, queryset=None):
        return ShoppingListItem.objects.get(pk=self.kwargs['item_pk'])

    def get_success_url(self):
        return reverse('shoppinglist_items', kwargs={'pk': self.kwargs['pk']})

class ShoppingListItemDeleteView(DeleteView):
    model = ShoppingListItem
    template_name = 'shoppinglist_item/shoppinglist_item_delete.html'

    def get_success_url(self):
        return reverse('shoppinglist_items', kwargs={'pk': self.kwargs['pk']})

@require_POST
def toggle_item_purchased(request, pk, item_pk):
    item = ShoppingListItem.objects.get(pk=item_pk, shopping_list_id=pk)
    item.is_purchased = not item.is_purchased
    item.save()
    return HttpResponseRedirect(reverse('shoppinglist_items', kwargs={'pk': pk}))

@csrf_exempt
def update_item_fields(request, pk, item_pk):
    item = ShoppingListItem.objects.get(pk=item_pk, shopping_list_id=pk)
    updated = False
    if request.method == 'POST':
        if 'is_purchased' in request.POST:
            item.is_purchased = True
            updated = True
        else:
            # Checkbox nicht im POST = nicht angehakt
            item.is_purchased = False
            updated = True
        if 'quantity' in request.POST:
            try:
                new_quantity = int(request.POST['quantity'])
                if new_quantity > 0 and new_quantity != item.quantity:
                    item.quantity = new_quantity
                    updated = True
            except ValueError:
                pass
        if updated:
            item.save()
    return HttpResponseRedirect(reverse('shoppinglist_items', kwargs={'pk': pk}))
