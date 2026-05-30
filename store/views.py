import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Product, Category, Metal, Purity, Order, Discount, KeyValueStore, Wishlist
from .cart import Cart
from django.utils import timezone
from django.core.cache import cache

CACHE_TTL = 300  # 5 minutes


def _get_kv(key, default=None):
    val = cache.get(f'kv_{key}')
    if val is None:
        try:
            val = KeyValueStore.objects.get(key=key).value
        except KeyValueStore.DoesNotExist:
            val = default or {}
        cache.set(f'kv_{key}', val, CACHE_TTL)
    return val


def get_homepage_content():
    return _get_kv('homepage_content')


def get_shop_content():
    return _get_kv('shop_page_content')


def get_footer_content():
    return _get_kv('footer_content')


def get_theme_settings():
    return _get_kv('theme_settings', {'activeHomepageTheme': 'default', 'activeProductTheme': 'default'})


def get_minimalist_content():
    return _get_kv('minimalist_homepage_content')


def homepage(request):
    from blog.models import BlogPost

    # Cache the full homepage context data
    cached = cache.get('homepage_data')
    if cached is None:
        theme_settings = get_theme_settings()
        active_theme = theme_settings.get('activeHomepageTheme', 'default')
        newest_products = list(Product.objects.filter(is_active=True).order_by('-created_at')[:10])
        best_sellers = list(Product.objects.filter(is_active=True).order_by('-display_price')[:10])
        blog_posts = list(BlogPost.objects.filter(status='published').order_by('-published_at')[:3])
        cached = {
            'theme_settings': theme_settings,
            'active_theme': active_theme,
            'newest_products': newest_products,
            'best_sellers': best_sellers,
            'blog_posts': blog_posts,
        }
        cache.set('homepage_data', cached, CACHE_TTL)

    context = dict(cached)
    context['homepage_content'] = get_homepage_content()
    context['minimalist_content'] = get_minimalist_content() if cached['active_theme'] == 'minimalist' else {}
    context['footer_content'] = get_footer_content()
    return render(request, 'store/homepage.html', context)


def shop(request):
    shop_content = get_shop_content()
    all_products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    metals = Metal.objects.filter(is_active=True)
    purities = Purity.objects.filter(is_active=True)

    category_id = request.GET.get('category')
    metal_id = request.GET.get('metal')
    purity_id = request.GET.get('purity')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_q = request.GET.get('q')
    sort_by = request.GET.get('sort', 'newest')

    if category_id:
        all_products = all_products.filter(categories__id=category_id)
    if metal_id:
        all_products = all_products.filter(metal__id=metal_id)
    if purity_id:
        all_products = all_products.filter(purity__id=purity_id)
    if min_price:
        all_products = all_products.filter(display_price__gte=float(min_price))
    if max_price:
        all_products = all_products.filter(display_price__lte=float(max_price))
    if search_q:
        all_products = all_products.filter(Q(name__icontains=search_q) | Q(description__icontains=search_q))

    if sort_by == 'price_asc':
        all_products = all_products.order_by('display_price')
    elif sort_by == 'price_desc':
        all_products = all_products.order_by('-display_price')
    elif sort_by == 'name':
        all_products = all_products.order_by('name')
    else:
        all_products = all_products.order_by('-created_at')

    context = {
        'shop_content': shop_content,
        'products': all_products,
        'categories': categories,
        'metals': metals,
        'purities': purities,
        'selected_category': category_id,
        'selected_metal': metal_id,
        'selected_purity': purity_id,
        'search_q': search_q or '',
        'sort_by': sort_by,
        'footer_content': get_footer_content(),
    }
    return render(request, 'store/shop.html', context)


def product_detail(request, product_id):
    from store.models import Metal, Purity, DiamondSeries
    import json
    product = get_object_or_404(Product, id=product_id, is_active=True)
    theme_settings = get_theme_settings()
    reviews = product.reviews.filter(status='approved')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    cross_sell = Product.objects.filter(id__in=product.cross_sell_products, is_active=True)
    upsell = Product.objects.filter(id__in=product.upsell_products, is_active=True)
    primary_category = product.categories.first()
    all_metals = Metal.objects.filter(is_active=True)
    all_purities = Purity.objects.filter(is_active=True).select_related('metal')
    diamond_series = DiamondSeries.objects.filter(is_active=True)

    in_wishlist = False
    if request.user.is_authenticated:
        try:
            wl = request.user.wishlist
            in_wishlist = product in wl.products.all()
        except Exception:
            pass

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
        'cross_sell_products': cross_sell,
        'upsell_products': upsell,
        'primary_category': primary_category,
        'theme_settings': theme_settings,
        'in_wishlist': in_wishlist,
        'footer_content': get_footer_content(),
        'all_metals': all_metals,
        'all_purities': all_purities,
        'diamond_series': diamond_series,
        'all_purities_json': json.dumps([{'id': p.id, 'label': p.label, 'fineness': p.fineness, 'metal_id': p.metal_id} for p in all_purities]),
        'all_metals_json': json.dumps([{'id': m.id, 'name': m.name, 'price_per_gram': m.price_per_gram} for m in all_metals]),
    }
    return render(request, 'store/product_detail.html', context)


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(categories=category, is_active=True)
    context = {
        'category': category,
        'products': products,
        'footer_content': get_footer_content(),
    }
    return render(request, 'store/category_products.html', context)


# ---- Cart Views ----

def cart_view(request):
    cart = Cart(request)
    subtotal = cart.get_subtotal()
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'cart_items': list(cart),
        'footer_content': get_footer_content(),
    }
    return render(request, 'store/cart.html', context)


@require_POST
def cart_add(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    variant = data.get('variant')
    price = data.get('price')
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product_id=product_id, quantity=quantity, variant=variant, price=price)
    return JsonResponse({'success': True, 'cart_count': len(cart)})


@require_POST
def cart_remove(request):
    data = json.loads(request.body)
    key = data.get('key')
    cart = Cart(request)
    cart.remove(key)
    return JsonResponse({'success': True, 'cart_count': len(cart)})


@require_POST
def cart_update(request):
    data = json.loads(request.body)
    key = data.get('key')
    quantity = int(data.get('quantity', 1))
    cart = Cart(request)
    cart.update(key, quantity)
    subtotal = cart.get_subtotal()
    return JsonResponse({'success': True, 'cart_count': len(cart), 'subtotal': subtotal})


# ---- Checkout ----

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store:cart')
    subtotal = cart.get_subtotal()
    user_addresses = []
    if request.user.is_authenticated:
        user_addresses = request.user.addresses or []
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'cart_items': list(cart),
        'user_addresses': user_addresses,
        'footer_content': get_footer_content(),
    }
    return render(request, 'store/checkout.html', context)


@require_POST
def apply_discount(request):
    data = json.loads(request.body)
    code = data.get('code', '').upper()
    subtotal = float(data.get('subtotal', 0))
    now = timezone.now()
    try:
        discount = Discount.objects.get(code__iexact=code, is_active=True)
        if discount.start_date and discount.start_date > now:
            return JsonResponse({'success': False, 'error': 'Discount not yet active'})
        if discount.end_date and discount.end_date < now:
            return JsonResponse({'success': False, 'error': 'Discount has expired'})
        if subtotal < discount.min_purchase:
            return JsonResponse({'success': False, 'error': f'Minimum purchase of ₹{int(discount.min_purchase)} required'})
        if discount.usage_limit and discount.usage_count >= discount.usage_limit:
            return JsonResponse({'success': False, 'error': 'Discount usage limit reached'})
        if discount.type == 'percentage':
            discount_amount = subtotal * (discount.value / 100)
        else:
            discount_amount = discount.value
        return JsonResponse({
            'success': True,
            'discount_amount': round(discount_amount),
            'discount_code': discount.code,
            'discount_type': discount.type,
            'discount_value': discount.value,
        })
    except Discount.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid discount code'})


@require_POST
def place_order(request):
    data = json.loads(request.body)
    cart = Cart(request)
    if len(cart) == 0:
        return JsonResponse({'success': False, 'error': 'Cart is empty'})

    shipping = data.get('shipping', {})
    discount_info = data.get('discount')
    subtotal = cart.get_subtotal()
    discount_amount = 0
    if discount_info:
        if discount_info.get('type') == 'percentage':
            discount_amount = subtotal * (discount_info['value'] / 100)
        else:
            discount_amount = discount_info.get('value', 0)
    total = subtotal - discount_amount

    items = []
    for item in cart:
        items.append({
            'product_id': item['product'].id,
            'product_name': item['product'].name,
            'quantity': item['quantity'],
            'price': item['price'],
            'variant': item['variant'],
            'image': item['product'].get_primary_image(),
        })

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        customer_name=shipping.get('name', ''),
        customer_email=shipping.get('email', ''),
        customer_phone=shipping.get('phone', ''),
        items=items,
        shipping_address=shipping,
        subtotal=subtotal,
        total=total,
        discount={'code': discount_info.get('code'), 'amount': discount_amount} if discount_info else {},
        payment_status='pending',
    )

    if discount_info and discount_info.get('code'):
        try:
            disc = Discount.objects.get(code__iexact=discount_info['code'])
            disc.usage_count += 1
            disc.save()
        except Discount.DoesNotExist:
            pass

    cart.clear()
    return JsonResponse({'success': True, 'order_id': order.id, 'total': total})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})


# ---- Wishlist ----

@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    context = {
        'wishlist': wishlist,
        'footer_content': get_footer_content(),
    }
    return render(request, 'store/wishlist.html', context)


@login_required
@require_POST
def wishlist_toggle(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        in_wishlist = False
    else:
        wishlist.products.add(product)
        in_wishlist = True
    return JsonResponse({'success': True, 'in_wishlist': in_wishlist})


@require_POST
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    from .models import ProductReview
    name = request.POST.get('name', '')
    rating = int(request.POST.get('rating', 5))
    text = request.POST.get('text', '')
    if name and text:
        ProductReview.objects.create(product=product, reviewer_name=name, rating=rating, text=text)
        messages.success(request, 'Review submitted! It will be visible after approval.')
    return redirect('store:product_detail', product_id=product_id)


def search_view(request):
    q = request.GET.get('q', '')
    products = Product.objects.none()
    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q), is_active=True
        )
    return render(request, 'store/search.html', {'products': products, 'query': q})


def contact_view(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you for contacting us. We will get back to you soon.')
        return redirect('store:contact')
    return render(request, 'store/contact.html', {'footer_content': get_footer_content()})
