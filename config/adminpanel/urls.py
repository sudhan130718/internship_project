from django.urls import path
from . import views





urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('users/', views.user_list, name='admin_users'),
    path('categories/', views.category_list, name='admin_categories'),
    path('brands/', views.brand_list, name='admin_brands'),
    path('products/', views.product_list, name='admin_products'),
    path('orders/', views.order_list, name='admin_orders'),

    path('api/categories/', views.category_list_create, name='api_category_list_create'),
    path('api/categories/<int:pk>/', views.category_detail, name='api_category_detail'),

    path('api/brands/', views.brand_list_create, name='brand_list_create'),
    path('api/brands/<int:pk>/', views.brand_update_delete, name='brand_update_delete'),

     path('api/products/', views.product_list_create, name='product_list_create'),
     path('api/products/<int:pk>/', views.product_update_delete, name='product_update_delete'),

    path('api/users/', views.user_list_api, name='user_list_api'),
    path('api/users/<int:pk>/', views.user_detail, name='api_user_detail'),

    path('api/orders/', views.order_list_api, name='order_list_api'), 
    path('api/orders/<int:order_id>/update_status/', views.update_order_status, name='update_order_status'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:order_id>/delete/', views.order_delete_view, name='order_delete'),
    path('orders/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),

    path('api/dashboard/', views.dashboard_data_api, name='dashboard_data_api'),

    
]

