from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('shop/', views.shop, name='shop'),
    path('products/<str:product_id>/', views.product_detail, name='product_detail'),
    path('products/<str:product_id>/review/', views.submit_review, name='submit_review'),
    path('category/<str:category_id>/', views.category_products, name='category_products'),
    path('search/', views.search_view, name='search'),
    path('contact/', views.contact_view, name='contact'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),
    path('cart/update/', views.cart_update, name='cart_update'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/apply-discount/', views.apply_discount, name='apply_discount'),
    path('checkout/place-order/', views.place_order, name='place_order'),
    path('order/<str:order_id>/success/', views.order_success, name='order_success'),

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/', views.wishlist_toggle, name='wishlist_toggle'),

    # Delivery check
    path('check-pincode/', views.check_pincode, name='check_pincode'),
]
