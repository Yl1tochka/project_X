from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product

def index(request):
    categories = Category.objects.all()
    # Добавим список категорий вручную, как на inyan.ru
    menu_categories = [
        "Сеты", "Сложные роллы", "Горячие роллы", "Запеченные роллы", "Классические роллы",
        "Суши, гунканы", "Пицца (32 см)", "Бургеры", "Салаты", "Супы", "Мясные и рыбные блюда",
        "Паста, вок", "Закуски", "Гарниры", "Детское меню", "Кофе", "Чаи", "Милкшейки",
        "Напитки", "Смузи и детоксы"
    ]
    return render(request, 'index.html', {'categories': categories, 'menu_categories': menu_categories})


# Меню
def menu(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'menu.html', {'categories': categories})


# Статичные страницы
def about(request): return render(request, 'about.html')


def delivery(request): return render(request, 'delivery.html')


def contacts(request): return render(request, 'contacts.html')


# --- Корзина ---
def cart_detail(request):
    categories = Category.objects.prefetch_related('products').all()
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        subtotal = float(product.price) * quantity
        image = product.image
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal
    return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total': total})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = {
        'quantity': cart.get(str(product_id), {}).get('quantity', 0) + 1,
        'price': str(product.price)
    }
    request.session['cart'] = cart
    messages.success(request, f"{product.name} добавлен в корзину!")
    return redirect('menu')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart_detail')


# --- Оформление заказа ---
def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        # Здесь будет отправка в Telegram (не вышло с первого раза)
        messages.success(request, "Заказ оформлен! Скоро с вами свяжемся 🍣")
        request.session['cart'] = {}  # очистка корзины
        return redirect('index')

    cart_items = []
    total = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        subtotal = float(product.price) * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'cart/order.html', {'cart_items': cart_items, 'total': total})