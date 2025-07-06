from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import ShoppingList, ShoppingListItem
from .forms import ShoppingListForm, ShoppingListUpdateForm, ShoppingListItemForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from stocks.models import StockList, StockListItem
from products.models import Product

from django.contrib import messages
from django.db import IntegrityError


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
        queryset = ShoppingListItem.objects.filter(shopping_list=self.shoppinglist)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(product__name__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoppinglist'] = ShoppingList.objects.get(pk=self.kwargs['pk'])
        context['request'] = self.request  # Damit {{ request.GET.q }} im Template funktioniert
        return context

  
class ShoppingListItemCreateView(CreateView):
    model = ShoppingListItem
    form_class = ShoppingListItemForm
    template_name = 'shoppinglist_item/shoppinglist_item_create.html'

    def post(self, request, *args, **kwargs):
        shoppinglist = ShoppingList.objects.get(pk=self.kwargs['pk'])
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity', 1)
        product = Product.objects.filter(name__iexact=product_name).first()
        if not product:
            try:
                # Passe die Default-Werte an dein Product-Modell an!
                product = Product.objects.create(
                    name=product_name,
                    price=0,  # Default-Wert, falls Pflichtfeld
                    # weitere Pflichtfelder mit Default-Werten ergänzen!
                )
            except IntegrityError:
                messages.error(request, "Produkt konnte nicht angelegt werden. Bitte alle Pflichtfelder prüfen.")
                return redirect('shoppinglist_items', pk=shoppinglist.pk)
        if ShoppingListItem.objects.filter(shopping_list=shoppinglist, product=product).exists():
            messages.error(request, "Dieses Produkt ist bereits auf der Liste.")
        else:
            ShoppingListItem.objects.create(
                shopping_list=shoppinglist,
                product=product,
                quantity=quantity
            )
        return redirect('shoppinglist_items', pk=shoppinglist.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoppinglist'] = ShoppingList.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        shoppinglist = ShoppingList.objects.get(pk=self.kwargs['pk'])
        form.instance.shopping_list = shoppinglist
        product = form.cleaned_data['product']
        # Prüfen, ob das Produkt schon existiert
        if ShoppingListItem.objects.filter(shopping_list=shoppinglist, product=product).exists():
            return self.render_to_response(self.get_context_data(
                form=form,
                error_message='Dieses Produkt ist bereits auf der Liste.'
            ))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shoppinglist_items', kwargs={'pk': self.kwargs['pk']})

def shoppinglist_item_create(request, pk):
    shoppinglist = get_object_or_404(ShoppingList, pk=pk)
    if request.method == 'POST':
        form = ShoppingListItemForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            if ShoppingListItem.objects.filter(shopping_list=shoppinglist, product=product).exists():
                return render(request, 'shoppinglist_item/shoppinglist_item_create.html', {
                    'form': form,
                    'shoppinglist': shoppinglist,
                    'error_message': 'Dieses Produkt ist bereits auf der Liste.'
                })


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

    def get_object(self, queryset=None):
        return ShoppingListItem.objects.get(pk=self.kwargs['item_pk'], shopping_list_id=self.kwargs['pk'])

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

def transfer_shoppinglist_to_stock(request, pk):
    shoppinglist = ShoppingList.objects.get(pk=pk)
    # Beispiel: Nimm die erste StockList des Users (oder biete Auswahl an)
    stocklists = StockList.objects.filter(owner=request.user)
    if not stocklists.exists():
        messages.error(request, "Du hast noch keine Vorratsliste.")
        return redirect('shoppinglist_items', pk=pk)
    stocklist = stocklists.first()  # Oder Auswahl anbieten

    items = ShoppingListItem.objects.filter(shopping_list=shoppinglist)
    count = 0
    for item in items:
        # Prüfe, ob das Produkt schon in der StockList ist
        stock_item, created = StockListItem.objects.get_or_create(
            stock_list=stocklist,
            product=item.product,
            defaults={'quantity': item.quantity, 'is_purchased': False}
        )
        if not created:
            # Falls schon vorhanden, erhöhe die Menge
            stock_item.quantity += item.quantity
            stock_item.save()
        count += 1
    messages.success(request, f"{count} Produkte wurden in die Vorratsliste übernommen.")
    return redirect('stocklist_items', pk=stocklist.pk)

def product_autocomplete(request):
    q = request.GET.get('term', '')
    print("AUTOCOMPLETE QUERY:", q)  # Debug
    products = Product.objects.filter(name__icontains=q).order_by('name')[:10]
    results = [{'id': p.id, 'label': p.name, 'value': p.name} for p in products]
    print("AUTOCOMPLETE RESULTS:", results)  # Debug
    return JsonResponse(results, safe=False)
