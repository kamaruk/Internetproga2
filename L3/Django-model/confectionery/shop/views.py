from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Cart, CartItem, Order
import stripe
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib import messages



# Главная страница
def index(request):
    return render(request, 'shop/index.html')

# Список продуктов
def product_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search', '')
    sort_price = request.GET.get('sort_price', '')

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort_price == 'asc':
        products = products.order_by('price')
    elif sort_price == 'desc':
        products = products.order_by('-price')

    return render(request, 'shop/product_list.html', {
        'products': products,
        'category': category,
        'search_query': search_query,
        'sort_price': sort_price,
    })

# Детали продукта
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# О нас
def about(request):
    return render(request, 'shop/about.html')

# Вход \ Регистрация
def auth_view(request):
    global form, signup_form
    if request.method == 'POST':
        if 'login' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect('index')
        elif 'signup' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()  # Форма входа
        signup_form = UserCreationForm()  # Форма регистрации

    return render(request, 'shop/auth.html', {'form': form, 'signup_form': signup_form})


@login_required(login_url='/auth/')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 0
    cart_item.save()

    return redirect('cart_detail')

# Корзина
@login_required
def update_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'items': items})

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

# Контакты
def contacts(request):
    return render(request, 'shop/contacts.html')


stripe.api_key = settings.STRIPE_SECRET_KEY

# Оплата
# Оплата
@login_required
def checkout(request):
    cart = request.user.cart
    items = cart.cartitem_set.all()

    total_rub = sum(item.product.price * item.quantity for item in items)

    if request.method == "POST":
        # Получаем данные из формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')  # Добавлен email

        if not email:  # Если email не был передан, добавьте сообщение об ошибке
            return render(request, 'shop/checkout.html', {
                'error_message': "Пожалуйста, укажите ваш email",
                'key': settings.STRIPE_PUBLISHABLE_KEY,
                'total': int(total_rub * 1),
                'total_rub': total_rub,
            })

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            email=email,  # Заполняем email
        )

        # Очищаем корзину после оформления заказа
        cart.cartitem_set.all().delete()

        # Редиректим на страницу успешного заказа
        return redirect('order_success')

    # Передаем данные в шаблон
    return render(request, 'shop/checkout.html', {
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'total': int(total_rub * 1),
        'total_rub': total_rub,
    })


# Проверка входа при добавлении в корзину
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def order_success(request):
    return render(request, 'shop/order_success.html')

