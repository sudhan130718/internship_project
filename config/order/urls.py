from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('track/<int:order_id>/', views.track_order, name='track_order'),
    path('order_history/', views.order_history, name='order_history'),
    
     path('wishlist_view/', views.wishlist_view, name='wishlist_view'),
    path('add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
 path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
 ]
