from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('',                    views.home,           name='home'),
    path('shop/',               views.shop,           name='shop'),
    path('product/<int:pk>/',   views.product_detail, name='product_detail'),

    # Cart
    path('cart/',                       views.cart_view,   name='cart'),
    path('cart/add/<int:pk>/',          views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/',       views.update_cart, name='update_cart'),
    path('cart/clear/',                 views.clear_cart,  name='clear_cart'),

    # Orders
    path('checkout/',                   views.checkout,      name='checkout'),
    path('place-order/',                views.place_order,   name='place_order'),
    path('order-success/<int:pk>/',     views.order_success, name='order_success'),
    path('my-orders/',                  views.my_orders,     name='my_orders'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
]
