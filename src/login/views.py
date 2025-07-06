from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from datetime import datetime
from .forms import NewUserForm, UsernameChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .tokens import account_activation_token
from django.contrib.auth.models import User
from shoppinglists.models import ShoppingList
from stocks.models import StockList
from products.models import Product

def home_view(request):
    return render(request, 'login/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'login/dashboard.html')

def register_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            # Send activation email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = request.build_absolute_uri(
                f"/activate/{uid}/{token}/"
            )
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(
                'Activate your account',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('home')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = NewUserForm()
    return render(request, 'login/register.html', context={'form': form})


@login_required
def username_change_view(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Benutzername geändert.')
            return redirect('dashboard')
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'login/username_change.html', {'form': form})

@login_required
def profile_edit_view(request):  # Entfernen Sie den doppelten @login_required
    if request.method == 'POST':
        # Account löschen
        if 'delete_account_confirm' in request.POST:
            confirmation_text = request.POST.get('confirmation_text', '').strip().upper()
            if confirmation_text == 'LÖSCHEN':
                try:
                    user = request.user
                    # Alle verwandten Daten löschen
                    
                    
                    ShoppingList.objects.filter(user=user).delete()
                    StockList.objects.filter(owner=user).delete()
                    Product.objects.filter(user=user).delete()
                    
                    # User löschen
                    user.delete()
                    messages.success(request, 'Ihr Account wurde erfolgreich gelöscht.')
                    return redirect('home')
                except Exception as e:
                    messages.error(request, f'Fehler beim Löschen des Accounts: {str(e)}')
            else:
                messages.error(request, 'Bestätigung fehlgeschlagen. Geben Sie exakt "LÖSCHEN" ein.')
                return render(request, 'login/account_delete_confirm.html')
        
        # Bestätigung anzeigen
        elif request.GET.get('delete_account') == '1':
            return render(request, 'login/account_delete_confirm.html')
        
        # Username ändern
        elif 'username_submit' in request.POST:
            username_form = UsernameChangeForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Benutzername erfolgreich geändert!')
                return redirect('profile_edit')
            else:
                messages.error(request, 'Fehler beim Ändern des Benutzernamens.')
        
        # Passwort ändern
        elif 'password_submit' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Passwort erfolgreich geändert!')
                return redirect('profile_edit')
            else:
                messages.error(request, 'Fehler beim Ändern des Passworts.')
    
    # GET Request - Formulare anzeigen
    username_form = UsernameChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    
    return render(request, 'login/profile_edit.html', {
        'username_form': username_form,
        'password_form': password_form,
    })

def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

def contact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")
        if email and message:
            
            send_mail(
                subject=f"Kontaktformular von {email}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
            messages.success(request, "Danke für deine Nachricht!")
        else:
            messages.error(request, "Bitte alle Felder ausfüllen.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def export_user_data(request):
    """
    Exportiert alle Benutzerdaten im JSON-Format gemäß DSGVO Art. 20
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        user = request.user
        user_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'user_id': user.id,
                'export_version': '1.0'
            },
            'account_data': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_active': user.is_active,
            },
            'application_data': {}
        }
        
        # KORRIGIERT: Verwende die richtigen Modelle aus Ihrem Code
        try:
            from shoppinglists.models import ShoppingList, ShoppingListItem
            shopping_lists = ShoppingList.objects.filter(user=user)
            user_data['application_data']['shopping_lists'] = []
            
            for shopping_list in shopping_lists:
                list_data = {
                    'name': shopping_list.name,
                    'created_at': shopping_list.created_at.isoformat() if hasattr(shopping_list, 'created_at') else None,
                    'items': []
                }
                
                items = ShoppingListItem.objects.filter(shopping_list=shopping_list)
                for item in items:
                    list_data['items'].append({
                        'product_name': item.product.name if item.product else 'Unbekannt',
                        'quantity': item.quantity,
                        'is_purchased': item.is_purchased,
                    })
                
                user_data['application_data']['shopping_lists'].append(list_data)
        except ImportError:
            pass
        
        # KORRIGIERT: Verwende StockList statt Stock
        try:
            from stocks.models import StockList, StockListItem
            stock_lists = StockList.objects.filter(owner=user)
            user_data['application_data']['stock_lists'] = []
            
            for stock_list in stock_lists:
                stock_data = {
                    'name': stock_list.name,
                    'created_at': stock_list.created_at.isoformat() if hasattr(stock_list, 'created_at') else None,
                    'items': []
                }
                
                items = StockListItem.objects.filter(stock_list=stock_list)
                for item in items:
                    stock_data['items'].append({
                        'product_name': item.product.name if item.product else 'Unbekannt',
                        'quantity': item.quantity,
                        'is_purchased': item.is_purchased,
                    })
                
                user_data['application_data']['stock_lists'].append(stock_data)
        except ImportError:
            pass
        
        # Produkte hinzufügen
        try:
            from products.models import Product
            products = Product.objects.filter(user=user)
            user_data['application_data']['products'] = []
            
            for product in products:
                user_data['application_data']['products'].append({
                    'name': product.name,
                    'category': product.category if hasattr(product, 'category') else None,
                    'created_at': product.created_at.isoformat() if hasattr(product, 'created_at') else None,
                })
        except ImportError:
            pass
        
        # JSON-Antwort mit korrekten Headers für Download
        response = HttpResponse(
            json.dumps(user_data, indent=2, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="meine-daten-kidme-{user.username}-{datetime.now().strftime("%Y%m%d")}.json"'
        
        return response
        
    except Exception as e:
        # Für Debugging
        import traceback
        print(f"Export Error: {e}")
        print(traceback.format_exc())
        return JsonResponse({'error': 'Export fehlgeschlagen', 'details': str(e)}, status=500)