from django.contrib import admin
from .models import Category,Brand, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  
    list_display = ['name', 'category', 'brand', 'mrp', 'selling_price', 'sku', 'instock','is_new_arrival', 'is_free_delivery']
    list_filter = ['category', 'instock', 'is_free_delivery']
    search_fields = ['name', 'sku']
