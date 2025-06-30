from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price')
    can_delete = False

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'cart_total')
    readonly_fields = ('created_at',)
    inlines = [CartItemInline]

    def cart_total(self, obj):
        return obj.total_price()
    cart_total.short_description = 'Cart Total'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'total_price')
    readonly_fields = ('total_price',)
    search_fields = ('product__name', 'cart__user__username')

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'
