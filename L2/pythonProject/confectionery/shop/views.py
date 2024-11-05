from django.http import HttpResponse
import json
from django.shortcuts import render
from django.conf import settings
import os

# Главная страница
def index(request):
    return render(request, 'shop/index.html')

# Страница "О нас"
def about(request):
    return render(request, 'shop/about.html')


# Страница продуктов
def products(request):

    json_path = os.path.join(settings.BASE_DIR, 'shop', 'products.json')

    with open(json_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    categories = list(set(product["category"] for product in products))

    context = {'categories': categories}
    return render(request, 'shop/products.html', context)


# Страница с деталями о продукте, переменная id
def product_detail(request, id):
    json_path = os.path.join(settings.BASE_DIR, 'shop', 'products.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    product = next((item for item in products if item['id'] == id), None)
    if product is None:
        return HttpResponse("Продукт не найден", status=404)

    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)


# Страница категории, переменная name
def category(request, name):

    json_path = os.path.join(settings.BASE_DIR, 'shop', 'products.json')

    with open(json_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    category_products = [product for product in products if product["category"] == name]

    context = {
        'products': category_products,
        'category_name': name
    }
    return render(request, 'shop/category.html', context)