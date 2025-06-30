from django.shortcuts import get_object_or_404, render, redirect
from .models import Brand, Category, Product,Review
from django.db.models import Sum, Q
from order.models import OrderItem, Wishlist
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def category_grid_view(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'products/category_grid.html', {'categories': categories,'brands': brands, })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_section.html', {'categories': categories})


def wholesale_deals_view(request):
    products = Product.objects.filter(is_wholesale=True)
    brands = Brand.objects.all()
    wishlist_product_ids = []
    if request.user.is_authenticated:
     wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    return render(request, 'products/wholesale_deals.html', {'products': products,'brands': brands,
        'wishlist_product_ids': wishlist_product_ids,
     })


def new_arrivals_list(request):
    new_arrivals = Product.objects.filter(is_new_arrival=True)

    # Filtering logic
    
    brand_ids = request.GET.getlist('brand')
    age_groups = request.GET.getlist('age')
    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 10000)
    

    


    

    if brand_ids:
        new_arrivals = new_arrivals.filter(brand__id__in=brand_ids)
    if age_groups:
        new_arrivals = new_arrivals.filter(ages__in=age_groups)

    if price_min != 0 or price_max != 10000:
       new_arrivals = new_arrivals.filter(selling_price__gte=price_min, selling_price__lte=price_max)
   
    brands = Brand.objects.all()
    age_choices = Product.AGE_CHOICES

    wishlist_product_ids = []
    if request.user.is_authenticated:
     wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)     

    return render(request, 'products/new_arrival.html', {
        'new_arrivals': new_arrivals,
        'brands': brands,
        'age_choices': age_choices,
        'selected_brands': brand_ids,
        'selected_ages': age_groups,
        'price_min': price_min,
        'price_max': price_max,
        'wishlist_product_ids': wishlist_product_ids,
    })



def product_list(request):
    products = Product.objects.all()

    # Get filters
  
    brand_ids = request.GET.getlist('brand')
    age_groups = request.GET.getlist('age')
    query = request.GET.get('q', '')

    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 10000)
    

    
   

    if price_min != 0 or price_max != 10000:
       products = products.filter(selling_price__gte=price_min, selling_price__lte=price_max)
   
   

    # Apply filters
    if brand_ids:
        products = products.filter(brand__id__in=brand_ids)

    if age_groups:
        products = products.filter(ages__in=age_groups)

   
  

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()

    brands = Brand.objects.all()
    age_choices = Product.AGE_CHOICES

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'products/products-list.html', {
        'query': query,
        'products': products,
        'brands': brands,
        'age_choices': age_choices,
        'selected_brands': brand_ids,
        'selected_ages': age_groups,
        'price_min': price_min,
        'price_max': price_max,
        'wishlist_product_ids': wishlist_product_ids,
    })


def products_by_category(request, slug):
    products = Product.objects.all()

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

     # Filtering logic
    brand_ids = request.GET.getlist('brand')
    age_groups = request.GET.getlist('age')

    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 10000)
    

    


    if price_min != 0 or price_max != 10000:
       products = products.filter(selling_price__gte=price_min, selling_price__lte=price_max)

    if brand_ids:
        products = products.filter(brand__id__in=brand_ids)
    if age_groups:
        products = products.filter(ages__in=age_groups)
    
    brands = Brand.objects.all()
    age_choices = Product.AGE_CHOICES

    query = request.GET.get('q', '')
   

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()

   
     
    return render(request, 'products/products-list.html', {
        'products': products,
        'selected_category': category,
        'brands': brands,
        'age_choices': age_choices,
        'selected_brands': brand_ids,
        'selected_ages': age_groups,
        'price_min': price_min,
        'price_max': price_max,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    brands = Brand.objects.all()

    pageDisplay = {
        'product': product,
        'brands': brands,
        'star_range': range(1, 6),  # Pass 1 to 5
    }
  
    return render(request, 'products/product_view.html' , pageDisplay)




def best_sellers_view(request):
    # Start with base queryset
    best_sellers = Product.objects.filter(sold_count__gt=0).order_by('-sold_count')

    # Filtering logic
    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 10000)
    brand_ids = request.GET.getlist('brand')
    age_groups = request.GET.getlist('age')

    if brand_ids:
        best_sellers = best_sellers.filter(brand__id__in=brand_ids)
    if age_groups:
        best_sellers = best_sellers.filter(ages__in=age_groups)
    if price_min != 0 or price_max != 10000:
       best_sellers = best_sellers.filter(selling_price__gte=price_min, selling_price__lte=price_max)

    # Search query
    query = request.GET.get('q', '')
    if query:
        best_sellers = best_sellers.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()

        wishlist_product_ids = []
    if request.user.is_authenticated:
     wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    # Apply slice *after* all filtering
    best_sellers = best_sellers[:10]

    # Supporting data
    brands = Brand.objects.all()
    age_choices = Product.AGE_CHOICES

    return render(request, 'products/best_sellers.html', {
        'best_sellers': best_sellers,
        'brands': brands,
        'age_choices': age_choices,
        'selected_brands': brand_ids,
        'selected_ages': age_groups,
        'price_min': price_min,
        'price_max': price_max,
                'wishlist_product_ids': wishlist_product_ids,

    })


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request,  {'form': form, 'product': product})

