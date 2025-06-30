from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


from rest_framework.decorators import api_view
from rest_framework import status
from products.models import Brand, Category
from products.models import Product
from order.models import  Order, OrderItem

from .serializers import CategorySerializer,BrandSerializer,ProductSerializer,AdminUserSerializer,OrderItemSerializer,OrderSerializer


from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

# Check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')


@user_passes_test(is_admin)
def user_list(request):
    return render(request, 'adminpanel/users.html')

@user_passes_test(is_admin)
def category_list(request):
    return render(request, 'adminpanel/categories.html')

@user_passes_test(is_admin)
def brand_list(request):
    return render(request, 'adminpanel/brands.html')

@user_passes_test(is_admin)
def product_list(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    age_choices = Product.AGE_CHOICES

    return render(request, 'adminpanel/products.html', {
        'categories': categories,
        'brands': brands,
        'age_choices':age_choices
    })

@user_passes_test(is_admin)
def order_list(request):
    return render(request, 'adminpanel/orders.html')






@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        categories = Category.objects.all()

        if search_query:
            categories = categories.filter(name__icontains=search_query)

        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get('page_size', 5))  # default 5
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)
       
        return paginator.get_paginated_response(serializer.data)
    
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        print("DATA:", request.data)
        print("FILES:", request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Deleted successfully'})
    

    # Brand

@api_view(['GET', 'POST'])
def brand_list_create(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        brands = Brand.objects.all()

        if search_query:
            brands = brands.filter(name__icontains=search_query)

        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get('page_size', 5))  # default 5
        result_page = paginator.paginate_queryset(brands, request)
        serializer = BrandSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BrandSerializer(data=request.data)
        print("DATA:", request.data)
        print("FILES:", request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def brand_update_delete(request, pk):
    try:
        brand = Brand.objects.get(pk=pk)
    except Brand.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


# Product

@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        products = Product.objects.all().order_by('-id')

        if search_query:
            products = products.filter(name__icontains=search_query)

        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get('page_size', 5))  # default 5
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
       
        serializer = ProductSerializer(data=request.data)
        print("DATA:", request.data)
        print("FILES:", request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['PUT', 'DELETE'])
def product_update_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    # users





@api_view(['GET', 'POST'])
def user_list_api(request):
 if request.method == 'GET':
    search_query = request.GET.get('search', '')
    users = User.objects.all().order_by('-id')  
    if search_query:
            users = users.filter(username__icontains=search_query)
    paginator = PageNumberPagination()
    paginator.page_size = int(request.GET.get('page_size', 5))
    result_page = paginator.paginate_queryset(users, request)
    serializer = AdminUserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

 elif request.method == 'POST':
        serializer = AdminUserSerializer(data=request.data)
        print("DATA:", request.data)
        print("FILES:", request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        serializer = AdminUserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AdminUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'Deleted successfully'})
    
    # Orders

from django.db.models import Q

@api_view(['GET'])
def order_list_api(request):
    search_query = request.GET.get('search', '')
    orders = Order.objects.all().order_by('-id')

    if search_query:
        orders = orders.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    paginator = PageNumberPagination()
    paginator.page_size = int(request.GET.get('page_size', 2))
    result_page = paginator.paginate_queryset(orders, request)

    serializer = OrderSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.data.get("status")

        valid_statuses = ['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED']
        if new_status not in valid_statuses:
            return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({'success': True})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    return render(request, 'adminpanel/order_detail.html', {
        'order': order,
        'order_items': order_items
    })



def order_delete_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'DELETE':
        order.delete()
        messages.success(request, "Order deleted successfully.")
        return redirect('order_list')  # update with your actual order list view name

    # If user tries to access directly via GET
    messages.warning(request, "Delete operation must be a POST request.")
    return redirect('order_detail', order_id=order_id)

# dashboard
@api_view(['GET'])
def dashboard_data_api(request):
    total_categories = Category.objects.count()
    total_brands = Brand.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()
    recent_orders = Order.objects.order_by('-id')[:5]

    data = {
        'total_categories':total_categories,
        'total_brands': total_brands,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': [
            {
                'id': o.id,
                'full_name': o.full_name,
                'total_amount': str(o.total_amount),
                'status': o.status
            } for o in recent_orders
        ]
    }
    return Response(data)

# Generate PDF

# adminpanel/views.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from order.models import Order

def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()  # related_name="items" used here

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    bold = styles["Heading4"]

    # 🧾 Title
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, y, f"INVOICE - Order #{order.id}")
    y -= 40

    # 📋 Order Details
    p.setFont("Helvetica", 12)
    p.drawString(40, y, f"Order Date: {order.order_date.strftime('%Y-%m-%d')}")
    y -= 20
    p.drawString(40, y, f"Customer: {order.user.username}")
    y -= 20
    p.drawString(40, y, f"Phone: {order.phone}")
    y -= 20
    p.drawString(40, y, f"Address: {order.address}")
    y -= 20
    p.drawString(40, y, f"Status: {order.status}")
    y -= 30

    # 🛍️ Product Table Header and Rows
    data = [['Product', 'Qty', 'Price']]
    for item in order_items:
        data.append([item.product.name, str(item.quantity), f"Rs {item.price:.2f}"])

    data.append(['', 'Total', f"Rs {order.total_amount:.2f}"])

    # 📐 Table Styling
    table = Table(data, colWidths=[240, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EED76D')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#131313')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # 👇 Draw the table
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, y - (20 * len(data)))  # adjust height based on row count

    # 📤 Save and return PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

    






