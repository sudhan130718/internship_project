from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_grid_view, name='category_grid'),
    
    path('new-arrivals/', views.new_arrivals_list, name='new_arrivals'),
    
    path('product_list/', views.product_list, name='product_list'),
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
   
    path('wholesale-deals/', views.wholesale_deals_view, name='wholesale_deals'),
    
    path('best-sellers/', views.best_sellers_view, name='best_sellers'),
    
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
]
