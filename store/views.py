from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Product, Category, Order, OrderItem


# ─────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────
def home(request):
    featured = Product.objects.filter(stock__gt=0)[:4]
    return render(request, 'store/home.html', {'featured': featured})


# ─────────────────────────────────────────
#  SHOP - product listing
# ─────────────────────────────────────────
def shop(request):
    products   = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    search     = request.GET.get('search', '')
    cat_id     = request.GET.get('category', '')

    if search:
        products = products.filter(name__icontains=search) | \
                   products.filter(description__icontains=search)

    if cat_id:
        products = products.filter(category_id=cat_id)

    return render(request, 'store/shop.html', {
        'products':   products,
        'categories': categories,
        'search':     search,
        'active_cat': cat_id,
    })


# ─────────────────────────────────────────
#  PRODUCT DETAIL
# ─────────────────────────────────────────
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


# ─────────────────────────────────────────
#  CART  (stored in session)
# ─────────────────────────────────────────
def cart_view(request):
    cart      = request.session.get('cart', {})
    cart_items = []
    subtotal  = 0

    for product_id, qty in cart.items():
        try:
            p = Product.objects.get(pk=product_id)
            line_total = p.price * qty
            subtotal  += float(line_total)
            cart_items.append({'product': p, 'quantity': qty, 'line_total': line_total})
        except Product.DoesNotExist:
            pass

    shipping = 0.0 if subtotal > 50 else (4.99 if subtotal > 0 else 0.0)
    total    = subtotal + shipping

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'subtotal':   subtotal,
        'shipping':   shipping,
        'total':      total,
    })


@require_POST
def add_to_cart(request, pk):
    product  = get_object_or_404(Product, pk=pk)
    cart     = request.session.get('cart', {})
    qty      = int(request.POST.get('quantity', 1))
    key      = str(pk)
    current  = cart.get(key, 0)

    if current + qty > product.stock:
        messages.error(request, f'Sorry! Only {product.stock} in stock.')
        return redirect('product_detail', pk=pk)

    cart[key] = current + qty
    request.session['cart'] = cart
    messages.success(request, f'🛒 {product.name} added to cart!')
    return redirect(request.POST.get('next', 'shop'))


@require_POST
def update_cart(request, pk):
    cart   = request.session.get('cart', {})
    key    = str(pk)
    action = request.POST.get('action')

    if action == 'increase':
        cart[key] = cart.get(key, 0) + 1
    elif action == 'decrease':
        cart[key] = cart.get(key, 1) - 1
        if cart[key] <= 0:
            del cart[key]
    elif action == 'remove':
        cart.pop(key, None)

    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def clear_cart(request):
    request.session['cart'] = {}
    messages.info(request, 'Cart cleared!')
    return redirect('cart')


# ─────────────────────────────────────────
#  CHECKOUT & ORDER
# ─────────────────────────────────────────
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    cart_items = []
    subtotal   = 0
    for product_id, qty in cart.items():
        try:
            p = Product.objects.get(pk=product_id)
            line_total = p.price * qty
            subtotal  += float(line_total)
            cart_items.append({'product': p, 'quantity': qty, 'line_total': line_total})
        except Product.DoesNotExist:
            pass

    shipping = 0.0 if subtotal > 50 else 4.99
    total    = subtotal + shipping

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'subtotal':   subtotal,
        'shipping':   shipping,
        'total':      total,
    })


@login_required
@require_POST
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    # Create the order
    order = Order.objects.create(user=request.user, total=0)

    for product_id, qty in cart.items():
        try:
            p = Product.objects.get(pk=product_id)
            if p.stock < qty:
                messages.error(request, f'Not enough stock for {p.name}!')
                order.delete()
                return redirect('cart')
            OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
            p.stock -= qty
            p.save()
        except Product.DoesNotExist:
            pass

    order.calculate_total()
    request.session['cart'] = {}   # clear cart
    messages.success(request, f'🎉 Order #{order.id} placed successfully!')
    return redirect('order_success', pk=order.id)


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})


# ─────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────
def register_view(request):
    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1:
            messages.error(request, 'All fields are required!')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match!')
        elif len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'That username is already taken!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'That email is already registered!')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'Welcome to Shopzy, {username}! 🎉')
            return redirect('home')

    return render(request, 'store/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {username}! 👋')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Wrong username or password!')

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out! See you soon 👋')
    return redirect('home')
