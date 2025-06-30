from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from products.models import Brand, Product
from .models import Order, OrderItem, Wishlist
from users.decorators import otp_required
from users.utils import send_otp_sms

from django.core.mail import send_mail


@login_required
@otp_required
@login_required
def place_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('checkout')

    cart_items = cart.items.all()
    cart_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address1=request.POST.get('address1')
        address2=request.POST.get('address2', '')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        payment_method = request.POST.get('payment_method')

        # Basic validation
        if not all([full_name, phone, address1,address2,city,state,pincode, payment_method]):
            messages.error(request, "Please fill in all fields.")
            return redirect('checkout')

        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address1=request.POST.get('address1'),
            address2=request.POST.get('address2'," "),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            payment_method=payment_method,
            total_amount=cart_total,
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.selling_price
            )
            # Update sold_count
            product = item.product
            product.sold_count += item.quantity
                # Deduct inventory
            product.total_stock -= item.quantity
            product.save()
        # Clear the cart
        print("product_names",item.product.name)

        product_names = ', '.join([item.product.name for item in cart.items.all()])  
        print("cart_items",cart.items.all())
      
        cart_items.delete()

        # ✅ Send confirmation email
        send_mail(
            subject="Order Successful",
            message = f"Wholesale Toy Website: Hi, {order.full_name}. Your order for {product_names} has been placed successfully.",

            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[request.user.email],
        fail_silently=False,    
        )

        # ✅ Send confirmation SMS
        phone = request.user.profile.phone_number
        if not phone.startswith('+'):
            phone = '+91' + phone

        send_otp_sms(
              phone,
              f"Wholesale Toy Website: Hi, {order.full_name}. Your order for {product_names} has been placed successfully."
              )
        messages.success(request, "Order placed successfully!")
        return redirect('order_success', order_id=order.id)

    return redirect('checkout')  # fallback for non-POST access




@login_required
@otp_required
def order_success(request, order_id):


     order = get_object_or_404(Order, id=order_id)

     order_items = order.items.all()
     brands = Brand.objects.all()

     return render(request, 'order/place_order.html', {
        'order': order,
        'order_items': order_items,
        'brands': brands,

    })

@login_required
@otp_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    brands = Brand.objects.all()

    return render(request, 'order/track_order.html', {'order': order,'brands': brands,
})


@login_required
@otp_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    brands = Brand.objects.all()

    return render(request, 'order/order_history.html', {'orders': orders,'brands': brands,
})

@login_required
@otp_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist_view')

@login_required
@otp_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist_view')

@login_required
@otp_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    print("Wishlist.objects", Wishlist.objects.filter(user=request.user))

    print("wishlist_items", wishlist_items)
    return render(request, 'order/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
@otp_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'wishlist_view'))
