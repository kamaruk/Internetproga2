from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('products/', views.product_list, name='product_list'),  # Список продуктов
    path('products/<int:pk>/', views.product_detail, name='product_detail'),  # Детали продукта
    path('about/', views.about, name='about'),  # О нас
    path('contacts/', views.contacts, name='contacts'),  # Контакты
    path('offers/', views.offers, name='offers'),  # Скидки
]
