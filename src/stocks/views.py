from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import StockList, StockListItem
from .forms import StockListForm, StockListUpdateForm, StockListItemForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


# StockView: List all stock lists for the logged-in user, including those shared with them.
class StockListView(LoginRequiredMixin, ListView):
    model = StockList
    form_class = StockListForm
    template_name = 'stocklist.html'
    context_object_name = 'stocklists'
    
    # Ensure the user is logged in before accessing this view
    def get_queryset(self):
        return StockList.objects.filter(Q(owner=self.request.user) | Q(shared_with=self.request.user)).distinct()


class StockListCreateView(LoginRequiredMixin, CreateView):
    model = StockList
    form_class = StockListForm
    template_name = 'stocklist_create.html'
    success_url = reverse_lazy('stocklists')
    

class StockListDeleteView(DeleteView):
    model = StockList
    success_url = reverse_lazy('stocklists')

class StockListUpdateView(UpdateView):
    model = StockList
    form_class = StockListUpdateForm
    template_name = 'stocklist_update.html'
    success_url = reverse_lazy('stocklists')

class StockListDetailView(LoginRequiredMixin, DetailView):
    model = StockList
    template_name = 'stocklist_detail.html'
    context_object_name = 'stocklists'

# StockItemView: List all items in a stock list, allowing the user to add new items.
class StockListItemView(LoginRequiredMixin, ListView):
    model = StockListItem
    template_name = 'stocklist_item/stocklist_item.html'
    context_object_name = 'stocklist_items'

    def get_queryset(self):
        # Richtig: Hole die StockList, nicht das einzelne Item!
        stocklist = StockList.objects.get(pk=self.kwargs['pk'])
        return StockListItem.objects.filter(stock_list=stocklist)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Kontext: Die aktuelle StockList
        context['stocklist'] = StockList.objects.get(pk=self.kwargs['pk'])
        return context

  
class StockListItemCreateView(LoginRequiredMixin, CreateView):
    model = StockListItem
    form_class = StockListItemForm
    template_name = 'stocklist_item/stocklist_item_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocklist'] = StockList.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        stocklist = StockList.objects.get(pk=self.kwargs['pk'])
        form.instance.stock_list = stocklist
        product = form.cleaned_data['product']
        # Prüfen, ob das Produkt schon existiert
        if StockListItem.objects.filter(stock_list=stocklist, product=product).exists():
            return self.render_to_response(self.get_context_data(
                form=form,
                error_message='Dieses Produkt ist bereits auf der Liste.'
            ))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stocklist_items', kwargs={'pk': self.kwargs['pk']})

class StockListItemUpdateView(LoginRequiredMixin, UpdateView):
    model = StockListItem
    form_class = StockListItemForm
    template_name = 'stocklist_item/stocklist_item_update.html'

    def get_object(self, queryset=None):
        return StockListItem.objects.get(pk=self.kwargs['item_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocklist'] = StockList.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('stocklist_items', kwargs={'pk': self.kwargs['pk']})

class StockListItemDeleteView(LoginRequiredMixin, DeleteView):
    model = StockListItem
    template_name = 'stocklist_item/stocklist_item_delete.html'

    def get_object(self, queryset=None):
        return StockListItem.objects.get(pk=self.kwargs['item_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocklist'] = StockList.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('stocklist_items', kwargs={'pk': self.kwargs['pk']})

@require_POST
def toggle_item_purchased(request, pk, item_pk):
    item = StockListItem.objects.get(pk=item_pk, stock_list_id=pk)
    item.is_purchased = not item.is_purchased
    item.save()
    return HttpResponseRedirect(reverse('stocklist_items', kwargs={'pk': pk}))

@csrf_exempt
def update_item_fields(request, pk, item_pk):
    item = StockListItem.objects.get(pk=item_pk, stock_list_id=pk)
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
    return HttpResponseRedirect(reverse('stocklist_items', kwargs={'pk': pk}))
