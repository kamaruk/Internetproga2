from django.shortcuts import render, get_object_or_404
from .models import Product

# Главная страница
def index(request):
    return render(request, 'shop/index.html')

# Список продуктов
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# Детали продукта
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# О нас
def about(request):
    return render(request, 'shop/about.html')

# Контакты
def contacts(request):
    return render(request, 'shop/contacts.html')

# Скидки
def offers(request):
    offers_data = [
        {'title': 'Скидка 10% на торты!', 'details': 'До конца месяца на все заказы торта предоставляется скидка.', 'expiry_date': '2024-11-30'},
        {'title': 'Бесплатная доставка', 'details': 'При заказе на сумму более 2000 рублей доставка бесплатна.', 'expiry_date': '2024-12-31'}
    ]
    return render(request, 'shop/offers.html', {'offers': offers_data})
