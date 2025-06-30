# adminpanel/serializers.py
from rest_framework import serializers
from products.models import Brand, Category
from products.models import Product
from django.contrib.auth.models import User
from order.models import  Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class BrandSerializer(serializers.ModelSerializer):
     
     class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'brand',
            'name',
            'slug',
            'image',
            'mrp',
            'selling_price',
            'sku',
            'instock',
            'return_available',
            'ages',
            'is_free_delivery',
            'delivery_charge',
            'is_new_arrival',
            'is_wholesale',
            'min_wholesale_quantity',
            'wholesale_price',
            'key_features',
            'description',
            'sold_count',
            'total_stock',
            'stock_threshold',
            'created_at',
        ]

class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'password']




class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # shows username
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_date', 'user', 'full_name', 'phone',
            'address', 'payment_method', 'status', 'total_amount',
            'items'
        ]        