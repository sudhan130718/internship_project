from django.shortcuts import render
from products.models import Brand, Category
from products.models import Product

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    new_arrivals = Product.objects.order_by('-created_at')[:12]
    brands = Brand.objects.all()
    return render(request, 'core/home.html', {
        'categories': categories,
        'products': products,
        'new_arrivals': new_arrivals,
        'brands': brands,
    })  

def delivery_info(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()
    return render(request, 'core/delivery_info.html', {
        'categories': categories,
        'products': products,
        'brands': brands,
    })     

def faqs(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()
    return render(request, 'core/faqs.html', {
        'categories': categories,
        'products': products,
        'brands': brands,
    })

def blog(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()
    return render(request, 'core/blog.html', {
        'categories': categories,
        'products': products,
        'brands': brands,
    })