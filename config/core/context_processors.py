from order.models import Wishlist
from products.models import Brand  # Adjust path as needed
from cart.models import Cart, CartItem

from django.db.models import Sum


def brand_context(request):
    return {
        # 'footer_brands': Brand.objects.all()
        'brands' : Brand.objects.all()
    }
def cart_item_count(request):
    count = 0
    print("request.session.get('otp_verified') =", request.session.get('otp_verified'))

    if request.user.is_authenticated and request.session.get('otp_verified'):
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    return {'cart_count': count}

    

def wishlist_count(request):
    count = 0
    if request.user.is_authenticated and request.session.get('otp_verified'):
        count = Wishlist.objects.filter(user=request.user).count()
    return {'wishlist_count': count}

