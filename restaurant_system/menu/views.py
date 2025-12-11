# menu/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .forms import CheckoutForm
from orders.models import Order, OrderItem
from delivery.models import Delivery


# ============================================
# API ViewSets (existants)
# ============================================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# ============================================
# Vues Templates pour les clients
# ============================================

def menu_list_view(request):
    """Affiche le menu avec possibilité de filtrer par catégorie"""
    category_slug = request.GET.get('category', 'all')
    
    # Récupérer toutes les catégories
    categories = Category.objects.all()
    
    # Filtrer les items selon la catégorie
    if category_slug == 'all':
        menu_items = MenuItem.objects.filter(available=True)
        current_category = 'all'
    else:
        category = get_object_or_404(Category, slug=category_slug)
        menu_items = MenuItem.objects.filter(category=category, available=True)
        current_category = category.slug
    
    # Gérer l'ajout au panier
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Initialiser le panier dans la session si nécessaire
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        cart = request.session['cart']
        
        # Ajouter ou mettre à jour la quantité
        if str(menu_item_id) in cart:
            cart[str(menu_item_id)] += quantity
        else:
            cart[str(menu_item_id)] = quantity
        
        request.session.modified = True
        messages.success(request, '✓ Plat ajouté au panier !')
        return redirect('menu-list')
    
    # Calculer le nombre d'articles dans le panier
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'current_category': current_category,
        'cart_count': cart_count,
    }
    return render(request, 'menu/menu_list.html', context)


def cart_view(request):
    """Affiche le panier et permet de modifier les quantités"""
    cart = request.session.get('cart', {})
    
    # Gérer la mise à jour du panier
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update':
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 0))
            
            if quantity > 0:
                cart[item_id] = quantity
            else:
                # Supprimer si quantité = 0
                cart.pop(item_id, None)
            
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Panier mis à jour !')
            return redirect('cart')
        
        elif action == 'clear':
            request.session['cart'] = {}
            request.session.modified = True
            messages.success(request, 'Panier vidé !')
            return redirect('cart')
    
    # Récupérer les détails des items du panier
    cart_items = []
    total = 0
    
    for item_id, quantity in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id, available=True)
            subtotal = menu_item.price * quantity
            cart_items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except MenuItem.DoesNotExist:
            # Supprimer l'item invalide du panier
            cart.pop(item_id, None)
            request.session.modified = True
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': sum(cart.values()),
    }
    return render(request, 'menu/cart.html', context)


def checkout_view(request):
    """Passer la commande"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, 'Votre panier est vide !')
        return redirect('menu-list')
    
    # Récupérer les détails du panier
    cart_items = []
    total = 0
    
    for item_id, quantity in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id, available=True)
            subtotal = menu_item.price * quantity
            cart_items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except MenuItem.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Créer la commande
            order = Order.objects.create(
                customer_name=form.cleaned_data['customer_name'],
                customer_phone=form.cleaned_data['customer_phone'],
                customer_email=form.cleaned_data['customer_email'],
                status='pending'
            )
            
            # Créer les items de la commande
            for item_data in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item_data['menu_item'],
                    quantity=item_data['quantity']
                )
            
            # Créer la livraison
            Delivery.objects.create(
                order=order,
                address=form.cleaned_data['address'],
                status='pending'
            )
            
            # Calculer le total de la commande
            order.calculate_total()
            
            # Vider le panier
            request.session['cart'] = {}
            request.session.modified = True
            
            messages.success(
                request, 
                f'✓ Commande #{order.id} passée avec succès ! Merci {order.customer_name} !'
            )
            return redirect('order-confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'cart_count': len(cart),
    }
    return render(request, 'menu/checkout.html', context)


def order_confirmation_view(request, order_id):
    """Page de confirmation de commande"""
    order = get_object_or_404(Order, id=order_id)
    delivery = Delivery.objects.get(order=order)
    
    context = {
        'order': order,
        'delivery': delivery,
    }
    return render(request, 'menu/order_confirmation.html', context)