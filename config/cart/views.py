from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404

from order.models import Wishlist
from products.models import Brand, Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from users.decorators import otp_required

@login_required
@otp_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')
    cart_total = cart.total_price()
    brands = Brand.objects.all()

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'brands': brands,

    })

from django.utils.http import url_has_allowed_host_and_scheme


@login_required
@otp_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    source = request.GET.get('source', 'other')  # 'wholesale' or 'other'

    is_wholesale = product.is_wholesale and source == 'wholesale'
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # ✅ Allow same product twice based on is_wholesale flag
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        is_wholesale=is_wholesale,  # 👈 key line that allows duplicates
        defaults={
            'quantity': 0,
            'price': product.wholesale_price if is_wholesale else product.selling_price
        }
    )
    print("cart_item.price:", cart_item.price)
    # Update quantity
    if created:
        cart_item.quantity = (
            product.min_wholesale_quantity if is_wholesale else quantity
        )
    else:
        cart_item.quantity += (
            product.min_wholesale_quantity if is_wholesale else quantity
        )
    Wishlist.objects.filter(user=request.user, product=product).delete()
    # Make sure price is correct
    cart_item.price = product.wholesale_price if is_wholesale else product.selling_price
    print("cart_item.price:", cart_item.price)
    cart_item.save()

    return redirect('cart_view')







from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import CartItem, Product

@login_required
@otp_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product = item.product  # Access product from the cart item

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            item.quantity += 1
            item.save()

        elif action == 'decrease':
            if product.is_wholesale:
                # Allow decrease only if quantity > min_wholesale_quantity
                if item.quantity > product.min_wholesale_quantity:
                    item.quantity -= 1
                    item.save()
            else:
                # For regular products, allow decrease if quantity > 1
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()

    return redirect('cart_view')


@login_required
@otp_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('cart_view')


@login_required
@otp_required
def checkout_view(request):
    brands = Brand.objects.all()
    cart_items = CartItem.objects.filter(cart__user=request.user)
    print("user", request.user)
    cart_total = sum(item.product.selling_price * item.quantity for item in cart_items)    
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'brands': brands,
    })


        



