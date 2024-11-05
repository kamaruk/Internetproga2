from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('category/<str:name>/', views.category, name='category'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]
