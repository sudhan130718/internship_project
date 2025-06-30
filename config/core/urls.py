from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('delivery_info', views.delivery_info, name='delivery_info'),
    path('faqs', views.faqs, name='faqs'),
    path('blog', views.blog, name='blog'),



]
