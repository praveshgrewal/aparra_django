import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.core.cache import cache
from functools import wraps


def clear_store_cache():
    cache.delete_many([
        'nav_categories', 'site_settings', 'homepage_data',
        'kv_homepage_content', 'kv_minimalist_homepage_content',
        'kv_theme_settings', 'kv_footer_content',
        'kv_shop_page_content', 'kv_site_settings', 'kv_settings',
    ])
from store.models import (
    Product, Category, Metal, Purity, TaxClass, Order, Discount,
    KeyValueStore, ProductReview, DiamondSeries, Menu
)
from accounts.models import User
from blog.models import BlogPost


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    today = timezone.now().date()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    today_sales = Order.objects.filter(created_at__date=today, payment_status='paid').aggregate(Sum('total'))['total__sum'] or 0
    today_cancellations = Order.objects.filter(created_at__date=today, status='cancelled').count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(Sum('total'))['total__sum'] or 0
    total_products = Product.objects.filter(is_active=True).count()
    total_customers = User.objects.filter(role='customer').count()
    new_signups_today = User.objects.filter(created_at__date=today).count()
    total_posts = BlogPost.objects.filter(status='published').count()
    recent_orders = Order.objects.order_by('-created_at')[:10]
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'today_sales': today_sales,
        'today_cancellations': today_cancellations,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_customers': total_customers,
        'new_signups_today': new_signups_today,
        'total_posts': total_posts,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)


# ---- Products ----

@admin_required
def product_list(request):
    products = Product.objects.select_related('metal', 'purity').all()
    search = request.GET.get('q')
    if search:
        products = products.filter(Q(name__icontains=search))
    return render(request, 'dashboard/products/list.html', {'products': products, 'search': search or ''})


@admin_required
def product_create(request):
    from store.models import DiamondSeries
    categories = Category.objects.filter(is_active=True)
    metals = Metal.objects.filter(is_active=True)
    purities = Purity.objects.filter(is_active=True)
    tax_classes = TaxClass.objects.filter(is_active=True)
    diamond_series = DiamondSeries.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        try:
            product = _save_product(request, None)
            messages.success(request, 'Product created successfully.')
            return redirect('dashboard:product_edit', product_id=product.id)
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'dashboard/products/form.html', {
        'categories': categories, 'metals': metals,
        'purities': purities, 'tax_classes': tax_classes,
        'diamond_series': diamond_series,
    })


@admin_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.filter(is_active=True)
    metals = Metal.objects.filter(is_active=True)
    purities = Purity.objects.filter(is_active=True)
    tax_classes = TaxClass.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            _save_product(request, product)
            messages.success(request, 'Product updated successfully.')
            return redirect('dashboard:product_edit', product_id=product.id)
        except Exception as e:
            messages.error(request, f'Error: {e}')

    import json as _json
    from store.models import DiamondSeries
    diamond_series = DiamondSeries.objects.filter(is_active=True).order_by('name')
    calculated_price = product.calculate_price() if product.auto_price_enabled else None
    all_products = list(Product.objects.filter(is_active=True).exclude(id=product.id).values('id', 'name'))
    # Use cross_sell_products as the single source; upsell mirrors it
    existing_related = list(dict.fromkeys(product.cross_sell_products or []))
    return render(request, 'dashboard/products/form.html', {
        'product': product, 'categories': categories,
        'metals': metals, 'purities': purities, 'tax_classes': tax_classes,
        'diamond_series': diamond_series,
        'calculated_price': calculated_price,
        'all_products_json': _json.dumps(all_products),
        'existing_related_json': _json.dumps(existing_related),
    })


def _save_product(request, product):
    p = request.POST
    if product is None:
        from store.models import generate_id
        product = Product(id=generate_id())

    product.name = p.get('name', '')
    product.description = p.get('description', '')
    product.seo_title = p.get('seo_title', '')
    product.seo_description = p.get('seo_description', '')
    product.meta_title = p.get('meta_title', '')
    product.meta_description = p.get('meta_description', '')
    product.more_info = p.get('more_info', '')
    if p.get('slug'):
        product.slug = p.get('slug', '')
    product.gross_weight = float(p.get('gross_weight', 0) or 0)
    product.net_weight = float(p.get('net_weight', 0) or 0)
    product.making_charge_type = p.get('making_charge_type', 'percentage')
    product.making_charge_value = float(p.get('making_charge_value', 0) or 0)
    product.auto_price_enabled = p.get('auto_price_enabled') == 'on'
    if p.get('manual_price'):
        product.manual_price = float(p.get('manual_price'))
    product.is_active = p.get('is_active') == 'on'
    product.has_diamonds = p.get('has_diamonds') == 'on'
    product.has_ring_size = p.get('has_ring_size') == 'on'
    product.has_stones = p.get('has_stones') == 'on'
    product.availability = p.get('availability', 'in_stock')
    disc = p.get('discount_percentage', '')
    product.discount_percentage = float(disc) if disc else None
    mc_disc = p.get('making_charge_discount', '')
    product.making_charge_discount = float(mc_disc) if mc_disc else None

    if p.get('metal_id'):
        try:
            product.metal = Metal.objects.get(id=p['metal_id'])
        except Metal.DoesNotExist:
            pass
    if p.get('purity_id'):
        try:
            product.purity = Purity.objects.get(id=p['purity_id'])
        except Purity.DoesNotExist:
            pass
    if p.get('tax_class_id'):
        try:
            product.tax_class = TaxClass.objects.get(id=p['tax_class_id'])
        except TaxClass.DoesNotExist:
            pass

    # Handle media as JSON array of URLs
    if p.get('media_json'):
        try:
            product.media = json.loads(p['media_json'])
        except Exception:
            pass

    # Handle diamond details JSON
    if p.get('diamond_details_json'):
        try:
            product.diamond_details = json.loads(p['diamond_details_json'])
        except Exception:
            pass

    # Related products
    if 'cross_sell_json' in p:
        try:
            product.cross_sell_products = json.loads(p['cross_sell_json']) or []
        except Exception:
            pass
    if 'upsell_json' in p:
        try:
            product.upsell_products = json.loads(p['upsell_json']) or []
        except Exception:
            pass

    # Recalculate price
    product.save()
    if product.auto_price_enabled:
        price = product.calculate_price()
        product.display_price = price
        product.save(update_fields=['display_price'])

    # Set categories
    cat_ids = request.POST.getlist('category_ids')
    if cat_ids:
        product.categories.set(Category.objects.filter(id__in=cat_ids))

    return product


@admin_required
@require_POST
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('dashboard:product_list')


@admin_required
@require_POST
def product_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = not product.is_active
    product.save(update_fields=['is_active'])
    return JsonResponse({'success': True, 'is_active': product.is_active})


# ---- Categories ----

@admin_required
def category_list(request):
    cats = Category.objects.all()
    return render(request, 'dashboard/categories/list.html', {'categories': cats})


@admin_required
def category_create(request):
    parents = Category.objects.filter(parent=None)
    if request.method == 'POST':
        from store.models import generate_id
        cat = Category(
            id=generate_id(),
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            image_url=request.POST.get('image_url', ''),
            is_active=request.POST.get('is_active') == 'on',
        )
        parent_id = request.POST.get('parent_id')
        if parent_id:
            try:
                cat.parent = Category.objects.get(id=parent_id)
            except Category.DoesNotExist:
                pass
        cat.save()
        clear_store_cache(); messages.success(request, 'Category created.')
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/categories/form.html', {'parents': parents})


@admin_required
def category_edit(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    parents = Category.objects.filter(parent=None).exclude(id=category_id)
    if request.method == 'POST':
        cat.name = request.POST.get('name', cat.name)
        cat.description = request.POST.get('description', '')
        cat.image_url = request.POST.get('image_url', '')
        cat.is_active = request.POST.get('is_active') == 'on'
        parent_id = request.POST.get('parent_id')
        if parent_id:
            try:
                cat.parent = Category.objects.get(id=parent_id)
            except Category.DoesNotExist:
                cat.parent = None
        else:
            cat.parent = None
        cat.save()
        messages.success(request, 'Category updated.')
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/categories/form.html', {'category': cat, 'parents': parents})


@admin_required
@require_POST
def category_delete(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    cat.delete()
    messages.success(request, 'Category deleted.')
    return redirect('dashboard:category_list')


# ---- Orders ----

@admin_required
def order_list(request):
    orders = Order.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'dashboard/orders/list.html', {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    })


@admin_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'dashboard/orders/detail.html', {'order': order})


@admin_required
@require_POST
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    status = request.POST.get('status')
    if status in dict(Order.STATUS_CHOICES):
        order.status = status
        order.save(update_fields=['status'])
        messages.success(request, 'Order status updated.')
    return redirect('dashboard:order_detail', order_id=order_id)


# ---- Customers ----

@admin_required
def customer_list(request):
    customers = User.objects.filter(role='customer').order_by('-created_at')
    return render(request, 'dashboard/customers/list.html', {'customers': customers})


@admin_required
def customer_detail(request, user_id):
    customer = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=customer).order_by('-created_at')
    return render(request, 'dashboard/customers/detail.html', {'customer': customer, 'orders': orders})


# ---- Blog ----

@admin_required
def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'dashboard/blog/list.html', {'posts': posts})


@admin_required
def blog_create(request):
    if request.method == 'POST':
        from store.models import generate_id
        from django.utils.text import slugify
        title = request.POST.get('title', '')
        slug = request.POST.get('slug') or slugify(title)
        if BlogPost.objects.filter(slug=slug).exists():
            slug = f"{slug}-{generate_id()}"
        post = BlogPost.objects.create(
            title=title,
            slug=slug,
            content=request.POST.get('content', ''),
            excerpt=request.POST.get('excerpt', ''),
            featured_image_url=request.POST.get('featured_image_url', ''),
            author=request.POST.get('author', request.user.name),
            status=request.POST.get('status', 'draft'),
        )
        if post.status == 'published':
            from django.utils import timezone
            post.published_at = timezone.now()
            post.save(update_fields=['published_at'])
        messages.success(request, 'Blog post created.')
        return redirect('dashboard:blog_edit', post_id=post.id)
    return render(request, 'dashboard/blog/form.html')


@admin_required
def blog_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        from django.utils.text import slugify
        post.title = request.POST.get('title', post.title)
        post.slug = request.POST.get('slug') or post.slug
        post.content = request.POST.get('content', post.content)
        post.excerpt = request.POST.get('excerpt', post.excerpt)
        post.featured_image_url = request.POST.get('featured_image_url', post.featured_image_url)
        post.author = request.POST.get('author', post.author)
        old_status = post.status
        post.status = request.POST.get('status', post.status)
        if post.status == 'published' and old_status != 'published':
            from django.utils import timezone
            post.published_at = timezone.now()
        post.save()
        messages.success(request, 'Blog post updated.')
        return redirect('dashboard:blog_edit', post_id=post.id)
    return render(request, 'dashboard/blog/form.html', {'post': post})


@admin_required
@require_POST
def blog_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    messages.success(request, 'Blog post deleted.')
    return redirect('dashboard:blog_list')


# ---- Metals & Purities ----

@admin_required
def metals_list(request):
    metals = Metal.objects.all()
    purities = Purity.objects.select_related('metal').all()
    return render(request, 'dashboard/metals/list.html', {'metals': metals, 'purities': purities})


@admin_required
@require_POST
def metal_save(request):
    metal_id = request.POST.get('metal_id')
    name = request.POST.get('name', '')
    price_per_gram = float(request.POST.get('price_per_gram', 0) or 0)
    is_active = request.POST.get('is_active') == 'on'
    if metal_id:
        metal = get_object_or_404(Metal, id=metal_id)
        metal.name = name
        metal.price_per_gram = price_per_gram
        metal.is_active = is_active
        metal.save()
        messages.success(request, 'Metal updated.')
    else:
        from store.models import generate_id
        Metal.objects.create(id=generate_id(), name=name, price_per_gram=price_per_gram, is_active=is_active)
        messages.success(request, 'Metal created.')
    referer = request.META.get('HTTP_REFERER', '')
    if 'pricing' in referer:
        return redirect('dashboard:pricing')
    return redirect('dashboard:metals_list')


@admin_required
@require_POST
def metal_delete(request, metal_id):
    metal = get_object_or_404(Metal, id=metal_id)
    metal.delete()
    messages.success(request, f'Metal "{metal.name}" deleted.')
    return redirect('dashboard:pricing')


@admin_required
@require_POST
def purity_save(request):
    purity_id = request.POST.get('purity_id')
    metal_id = request.POST.get('metal_id')

    # Handle delete from pricing page
    if request.POST.get('_delete') and purity_id:
        purity = get_object_or_404(Purity, id=purity_id)
        purity.delete()
        messages.success(request, 'Purity deleted.')
        referer = request.META.get('HTTP_REFERER', '')
        if 'pricing' in referer:
            return redirect('dashboard:pricing')
        return redirect('dashboard:metals_list')

    label = request.POST.get('label', '')
    fineness = float(request.POST.get('fineness', 0) or 0)
    # Auto-normalise: millesimal (e.g. 916) → 0.916, percentage (91.6) → 0.916
    if fineness > 100:
        fineness = fineness / 1000
    elif fineness > 1:
        fineness = fineness / 100
    is_active = request.POST.get('is_active') == 'on'
    metal = get_object_or_404(Metal, id=metal_id)
    if purity_id:
        purity = get_object_or_404(Purity, id=purity_id)
        purity.metal = metal
        purity.label = label
        purity.fineness = fineness
        purity.is_active = is_active
        purity.save()
        messages.success(request, 'Purity updated.')
    else:
        from store.models import generate_id
        Purity.objects.create(id=generate_id(), metal=metal, label=label, fineness=fineness, is_active=is_active)
        messages.success(request, 'Purity created.')
    referer = request.META.get('HTTP_REFERER', '')
    if 'pricing' in referer:
        return redirect('dashboard:pricing')
    return redirect('dashboard:metals_list')


# ---- Tax Classes ----

@admin_required
def tax_list(request):
    taxes = TaxClass.objects.all()
    return render(request, 'dashboard/taxes/list.html', {'taxes': taxes})


@admin_required
@require_POST
def tax_save(request):
    tax_id = request.POST.get('tax_id')
    name = request.POST.get('name', '')
    rate_type = request.POST.get('rate_type', 'percentage')
    rate_value = float(request.POST.get('rate_value', 0) or 0)
    is_active = request.POST.get('is_active') == 'on'
    if tax_id:
        tax = get_object_or_404(TaxClass, id=tax_id)
        tax.name = name
        tax.rate_type = rate_type
        tax.rate_value = rate_value
        tax.is_active = is_active
        tax.save()
        messages.success(request, 'Tax class updated.')
    else:
        from store.models import generate_id
        TaxClass.objects.create(id=generate_id(), name=name, rate_type=rate_type, rate_value=rate_value, is_active=is_active)
        messages.success(request, 'Tax class created.')
    return redirect('dashboard:tax_list')


# ---- Discounts ----

@admin_required
def discount_list(request):
    discounts = Discount.objects.all()
    return render(request, 'dashboard/discounts/list.html', {'discounts': discounts})


@admin_required
def discount_create(request):
    if request.method == 'POST':
        from store.models import generate_id
        Discount.objects.create(
            id=generate_id(),
            code=request.POST.get('code', '').upper(),
            type=request.POST.get('type', 'percentage'),
            value=float(request.POST.get('value', 0) or 0),
            min_purchase=float(request.POST.get('min_purchase', 0) or 0),
            is_active=request.POST.get('is_active') == 'on',
            usage_limit=int(request.POST.get('usage_limit') or 0) or None,
        )
        messages.success(request, 'Discount created.')
        return redirect('dashboard:discount_list')
    return render(request, 'dashboard/discounts/form.html')


@admin_required
@require_POST
def discount_delete(request, discount_id):
    disc = get_object_or_404(Discount, id=discount_id)
    disc.delete()
    messages.success(request, 'Discount deleted.')
    return redirect('dashboard:discount_list')


# ---- Reviews ----

@admin_required
def review_list(request):
    reviews = ProductReview.objects.select_related('product').all()
    status_filter = request.GET.get('status')
    if status_filter:
        reviews = reviews.filter(status=status_filter)
    return render(request, 'dashboard/reviews/list.html', {
        'reviews': reviews,
        'status_filter': status_filter,
    })


@admin_required
@require_POST
def review_update_status(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    status = request.POST.get('status', 'approved')
    review.status = status
    review.save(update_fields=['status'])
    return JsonResponse({'success': True})


@admin_required
@require_POST
def review_delete(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('dashboard:review_list')


# ---- Settings ----

@admin_required
def settings_view(request):
    try:
        kv = KeyValueStore.objects.get(key='settings')
        settings_data = kv.value
    except KeyValueStore.DoesNotExist:
        settings_data = {}
    return render(request, 'dashboard/settings/settings.html', {'settings_data': settings_data})


@admin_required
@require_POST
def settings_save(request):
    try:
        kv = KeyValueStore.objects.get(key='settings')
        settings_data = kv.value
    except KeyValueStore.DoesNotExist:
        kv = KeyValueStore(key='settings')
        settings_data = {}

    # WhatsApp settings
    settings_data['whatsapp'] = {
        'enabled': request.POST.get('whatsapp_enabled') == 'on',
        'phoneNumber': request.POST.get('whatsapp_phone', ''),
        'defaultMessage': request.POST.get('whatsapp_message', ''),
    }

    # Store info
    settings_data['store'] = {
        'name': request.POST.get('store_name', ''),
        'email': request.POST.get('store_email', ''),
        'phone': request.POST.get('store_phone', ''),
        'address': request.POST.get('store_address', ''),
        'currency': request.POST.get('currency', 'INR'),
    }

    kv.value = settings_data
    kv.save()
    clear_store_cache()
    messages.success(request, 'Settings saved.')
    return redirect('dashboard:settings')


# ---- Appearance / Theme ----

@admin_required
def appearance_view(request):
    def _get_kv(key, default=None):
        try:
            return KeyValueStore.objects.get(key=key).value
        except KeyValueStore.DoesNotExist:
            return default or {}

    theme_data = _get_kv('theme_settings')
    homepage_raw = _get_kv('homepage_content')
    footer_data = _get_kv('footer_content')
    site_data = _get_kv('site_settings')

    # Extract section list from layout for the homepage layout tab
    homepage_sections = homepage_raw.get('layout', []) if isinstance(homepage_raw, dict) else []

    import json as _json
    homepage_json = _json.dumps(homepage_raw, indent=2) if homepage_raw else '{}'

    return render(request, 'dashboard/appearance/appearance.html', {
        'theme_data': theme_data,
        'homepage_json': homepage_json,
        'homepage_sections': homepage_sections,
        'footer_data': footer_data,
        'site_data': site_data,
    })


@admin_required
@require_POST
def appearance_save(request):
    tab = request.POST.get('tab', 'theme')

    if tab == 'theme':
        kv, _ = KeyValueStore.objects.get_or_create(key='theme_settings')
        kv.value = {
            'activeHomepageTheme': request.POST.get('homepage_theme', 'default'),
            'activeProductTheme': request.POST.get('product_theme', 'default'),
            'primaryColor': request.POST.get('primary_color', '#b8860b'),
            'bgColor': request.POST.get('bg_color', '#f5f0e8'),
            'fgColor': request.POST.get('fg_color', '#3d2b1f'),
            'headingFont': request.POST.get('heading_font', 'Playfair Display'),
            'bodyFont': request.POST.get('body_font', 'Inter'),
        }
        kv.save()
        messages.success(request, 'Theme settings saved.')

    elif tab == 'homepage_json':
        import json as _json
        try:
            data = _json.loads(request.POST.get('homepage_json', '{}'))
            kv, _ = KeyValueStore.objects.get_or_create(key='homepage_content')
            kv.value = data
            kv.save()
            messages.success(request, 'Homepage content saved.')
        except Exception as e:
            messages.error(request, f'Invalid JSON: {e}')

    elif tab == 'section_toggle':
        kv, _ = KeyValueStore.objects.get_or_create(key='homepage_content')
        data = kv.value or {}
        layout = data.get('layout', [])
        section_id = request.POST.get('section_id')
        visible = request.POST.get('visible') == 'true'
        for s in layout:
            if s.get('id') == section_id:
                s['visible'] = visible
                break
        data['layout'] = layout
        kv.value = data
        kv.save()
        messages.success(request, 'Section updated.')

    elif tab == 'header':
        kv, _ = KeyValueStore.objects.get_or_create(key='site_settings')
        data = kv.value or {}
        data.update({
            'announcement_text': request.POST.get('announcement_text', ''),
            'announcement_url': request.POST.get('announcement_url', ''),
            'show_announcement': request.POST.get('show_announcement') == 'on',
            'whatsapp_number': request.POST.get('whatsapp_number', ''),
            'logo_url': request.POST.get('logo_url', ''),
        })
        kv.value = data
        kv.save()
        messages.success(request, 'Header settings saved.')

    elif tab == 'footer':
        kv, _ = KeyValueStore.objects.get_or_create(key='footer_content')
        data = kv.value or {}
        data.update({
            'tagline': request.POST.get('footer_tagline', ''),
            'email': request.POST.get('footer_email', ''),
            'phone': request.POST.get('footer_phone', ''),
            'address': request.POST.get('footer_address', ''),
            'copyright': request.POST.get('footer_copyright', ''),
            'social': {
                'instagram': request.POST.get('social_instagram', ''),
                'facebook': request.POST.get('social_facebook', ''),
                'youtube': request.POST.get('social_youtube', ''),
                'pinterest': request.POST.get('social_pinterest', ''),
            },
        })
        kv.value = data
        kv.save()
        messages.success(request, 'Footer settings saved.')

    clear_store_cache()
    return redirect('dashboard:appearance')


# ---- Media Manager ----

@admin_required
def media_view(request):
    import os
    from django.conf import settings
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    files = []
    for f in os.listdir(upload_dir):
        fpath = os.path.join(upload_dir, f)
        if os.path.isfile(fpath):
            files.append({'name': f, 'url': settings.MEDIA_URL + 'uploads/' + f})
    return render(request, 'dashboard/media/media.html', {'files': files})


@admin_required
def media_list_json(request):
    import os
    from django.conf import settings as django_settings
    upload_dir = os.path.join(django_settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    files = []
    for f in sorted(os.listdir(upload_dir), reverse=True):
        fpath = os.path.join(upload_dir, f)
        if os.path.isfile(fpath) and f.lower().split('.')[-1] in ('jpg','jpeg','png','webp','gif'):
            files.append({'name': f, 'url': django_settings.MEDIA_URL + 'uploads/' + f})
    return JsonResponse({'files': files})


@admin_required
@require_POST
def media_upload(request):
    import os
    from django.conf import settings
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    uploaded = []
    for f in request.FILES.getlist('files'):
        fname = f.name
        fpath = os.path.join(upload_dir, fname)
        with open(fpath, 'wb+') as dest:
            for chunk in f.chunks():
                dest.write(chunk)
        uploaded.append({'name': fname, 'url': settings.MEDIA_URL + 'uploads/' + fname})
    return JsonResponse({'success': True, 'files': uploaded})


# ---- Homepage Content ----

@admin_required
def homepage_content_view(request):
    try:
        kv = KeyValueStore.objects.get(key='homepage_content')
        content = kv.value
    except KeyValueStore.DoesNotExist:
        content = {}
    return render(request, 'dashboard/appearance/homepage_content.html', {'content': content})


@admin_required
@require_POST
def homepage_content_save(request):
    try:
        kv = KeyValueStore.objects.get(key='homepage_content')
    except KeyValueStore.DoesNotExist:
        kv = KeyValueStore(key='homepage_content')
    try:
        body = json.loads(request.body)
        kv.value = body
    except Exception:
        kv.value = {}
    kv.save()
    clear_store_cache()
    return JsonResponse({'success': True})


# ---- Pricing Management ----

@admin_required
def pricing_view(request):
    metals = Metal.objects.all().order_by('name')
    purities = Purity.objects.select_related('metal').all()
    diamond_series = DiamondSeries.objects.all().order_by('name')

    metals_with_purities = []
    for metal in metals:
        metals_with_purities.append({
            'metal': metal,
            'purities': [p for p in purities if p.metal_id == metal.id],
        })

    return render(request, 'dashboard/pricing/pricing.html', {
        'metals_with_purities': metals_with_purities,
        'metals': metals,
        'diamond_series': diamond_series,
    })


@admin_required
@require_POST
def pricing_save_metals(request):
    updated = 0
    for metal in Metal.objects.all():
        try:
            price_key = f'price_{metal.id}'
            active_key = f'active_{metal.id}'
            if price_key in request.POST:
                metal.price_per_gram = float(request.POST[price_key] or 0)
            metal.is_active = active_key in request.POST
            metal.save(update_fields=['price_per_gram', 'is_active'])
            updated += 1
        except Exception:
            pass
    # Recalculate all product prices
    from store.models import Product
    for product in Product.objects.filter(auto_price_enabled=True):
        price = product.calculate_price()
        if price:
            product.display_price = price
            product.save(update_fields=['display_price'])
    messages.success(request, f'Metal prices saved. {updated} metals updated, product prices recalculated.')
    return redirect('dashboard:pricing')


@admin_required
@require_POST
def diamond_series_save(request):
    from store.models import generate_id
    series_id = request.POST.get('series_id')
    name = request.POST.get('name', '').strip()
    if not name:
        messages.error(request, 'Series name is required.')
        return redirect('dashboard:pricing')

    if series_id:
        ds = get_object_or_404(DiamondSeries, id=series_id)
    else:
        ds = DiamondSeries(id=generate_id())

    ds.name = name
    ds.rate_per_carat = float(request.POST.get('rate_per_carat', 0) or 0)
    ds.description = request.POST.get('description', '')
    ds.diamond_type = request.POST.get('diamond_type', 'Both')
    ds.is_active = request.POST.get('is_active') == 'on'
    ds.cut = request.POST.get('cut', '')
    ds.color = request.POST.get('color', '')
    ds.clarity = request.POST.get('clarity', '')
    sc = request.POST.get('setting_charges', '')
    ds.setting_charges = float(sc) if sc else None
    cc = request.POST.get('certification_cost', '')
    ds.certification_cost = float(cc) if cc else None
    bm = request.POST.get('brand_margin', '')
    ds.brand_margin = float(bm) if bm else None
    ds.save()
    messages.success(request, f'Diamond series "{ds.name}" saved.')
    return redirect('dashboard:pricing')


@admin_required
@require_POST
def diamond_series_delete(request, series_id):
    ds = get_object_or_404(DiamondSeries, id=series_id)
    ds.delete()
    messages.success(request, 'Diamond series deleted.')
    return redirect('dashboard:pricing')


# ---- Reports / Analytics ----

@admin_required
def report_view(request):
    from datetime import timedelta, date
    from django.db.models.functions import TruncDate
    from django.db.models import Count

    period = request.GET.get('period', '30')
    days = int(period) if period in ('7', '30', '90') else 30
    since = timezone.now() - timedelta(days=days)

    daily_revenue = (
        Order.objects
        .filter(created_at__gte=since, payment_status='paid')
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(revenue=Sum('total'), count=Count('id'))
        .order_by('day')
    )

    labels = []
    revenues = []
    today = timezone.now().date()
    revenue_map = {r['day']: float(r['revenue']) for r in daily_revenue}
    count_map = {r['day']: r['count'] for r in daily_revenue}
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        labels.append(d.strftime('%d %b'))
        revenues.append(revenue_map.get(d, 0))

    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    status_data = {s['status']: s['count'] for s in status_counts}

    top_products = []
    for order in Order.objects.filter(created_at__gte=since).only('items'):
        for item in (order.items or []):
            found = False
            for tp in top_products:
                if tp['id'] == item.get('product_id'):
                    tp['qty'] += item.get('quantity', 1)
                    tp['revenue'] += item.get('price', 0) * item.get('quantity', 1)
                    found = True
                    break
            if not found:
                top_products.append({
                    'id': item.get('product_id'),
                    'name': item.get('name', 'Unknown'),
                    'qty': item.get('quantity', 1),
                    'revenue': item.get('price', 0) * item.get('quantity', 1),
                })
    top_products.sort(key=lambda x: x['revenue'], reverse=True)

    total_revenue = Order.objects.filter(payment_status='paid').aggregate(Sum('total'))['total__sum'] or 0
    total_orders = Order.objects.count()
    avg_order = total_revenue / total_orders if total_orders else 0

    context = {
        'labels_json': json.dumps(labels),
        'revenues_json': json.dumps(revenues),
        'status_data': status_data,
        'top_products': top_products[:10],
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'avg_order': avg_order,
        'period': period,
        'period_choices': [('7', 'Last 7 days'), ('30', 'Last 30 days'), ('90', 'Last 90 days')],
    }
    return render(request, 'dashboard/report/report.html', context)


# ---- Bulk Product Upload ----

@admin_required
def product_bulk_upload(request):
    return render(request, 'dashboard/products/bulk_upload.html')


@admin_required
@require_POST
def product_bulk_upload_process(request):
    import csv, io
    from store.models import generate_id
    from django.utils.text import slugify

    f = request.FILES.get('csv_file')
    if not f:
        messages.error(request, 'No file uploaded.')
        return redirect('dashboard:product_bulk_upload')

    decoded = f.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    created = 0
    errors = []

    for i, row in enumerate(reader, start=2):
        try:
            name = row.get('name', '').strip()
            if not name:
                errors.append(f'Row {i}: missing name')
                continue

            product = Product(id=generate_id())
            product.name = name
            product.description = row.get('description', '')
            product.gross_weight = float(row.get('gross_weight', 0) or 0)
            product.net_weight = float(row.get('net_weight', 0) or 0)
            product.making_charge_type = row.get('making_charge_type', 'percentage')
            product.making_charge_value = float(row.get('making_charge_value', 0) or 0)
            product.availability = row.get('availability', 'in_stock')
            product.is_active = str(row.get('is_active', 'true')).lower() not in ('false', '0', 'no')
            product.slug = row.get('slug') or slugify(name)

            manual_price = row.get('manual_price', '').strip()
            if manual_price:
                product.auto_price_enabled = False
                product.manual_price = float(manual_price)
            else:
                product.auto_price_enabled = True

            image_url = row.get('image_url', '').strip()
            if image_url:
                product.media = [{'url': image_url, 'type': 'image'}]

            metal_name = row.get('metal', '').strip()
            if metal_name:
                try:
                    product.metal = Metal.objects.get(name__iexact=metal_name)
                except Metal.DoesNotExist:
                    pass

            product.save()

            cat_names = [c.strip() for c in row.get('categories', '').split(',') if c.strip()]
            if cat_names:
                cats = Category.objects.filter(name__in=cat_names)
                product.categories.set(cats)

            if product.auto_price_enabled:
                price = product.calculate_price()
                if price:
                    product.display_price = price
                    product.save(update_fields=['display_price'])

            created += 1
        except Exception as e:
            errors.append(f'Row {i}: {e}')

    msg = f'Imported {created} products.'
    if errors:
        msg += f' {len(errors)} errors: ' + '; '.join(errors[:5])
        messages.warning(request, msg)
    else:
        messages.success(request, msg)
    return redirect('dashboard:product_list')


# ---- Shipping Settings ----

@admin_required
def shipping_view(request):
    try:
        kv = KeyValueStore.objects.get(key='shipping_settings')
        shipping = kv.value
    except KeyValueStore.DoesNotExist:
        shipping = {}
    return render(request, 'dashboard/shipping/shipping.html', {'shipping': shipping})


@admin_required
@require_POST
def shipping_save(request):
    kv, _ = KeyValueStore.objects.get_or_create(key='shipping_settings')
    raw_pins = request.POST.get('blocked_pincodes_raw', '')
    import re as _re
    blocked_pincodes = [p.strip() for p in _re.split(r'[\n,]+', raw_pins) if p.strip()]
    data = {
        'free_shipping_enabled': request.POST.get('free_shipping_enabled') == 'on',
        'free_shipping_threshold': float(request.POST.get('free_shipping_threshold', 0) or 0),
        'standard_rate': float(request.POST.get('standard_rate', 0) or 0),
        'express_rate': float(request.POST.get('express_rate', 0) or 0),
        'cod_enabled': request.POST.get('cod_enabled') == 'on',
        'cod_charge': float(request.POST.get('cod_charge', 0) or 0),
        'estimated_days_standard': request.POST.get('estimated_days_standard', '5-7'),
        'estimated_days_express': request.POST.get('estimated_days_express', '1-2'),
        'delivery_note': request.POST.get('delivery_note', ''),
        'blocked_pincodes': blocked_pincodes,
    }
    kv.value = data
    kv.save()
    messages.success(request, 'Shipping settings saved.')
    return redirect('dashboard:shipping')


# ---- Payment Settings ----

@admin_required
def payment_settings_view(request):
    try:
        kv = KeyValueStore.objects.get(key='payment_settings')
        payment = kv.value
    except KeyValueStore.DoesNotExist:
        payment = {}
    from django.conf import settings as django_settings
    payment.setdefault('razorpay_key_id', getattr(django_settings, 'RAZORPAY_KEY_ID', ''))
    return render(request, 'dashboard/settings/payment.html', {'payment': payment})


@admin_required
@require_POST
def payment_settings_save(request):
    kv, _ = KeyValueStore.objects.get_or_create(key='payment_settings')
    data = {
        'razorpay_key_id': request.POST.get('razorpay_key_id', ''),
        'razorpay_key_secret': request.POST.get('razorpay_key_secret', ''),
        'razorpay_enabled': request.POST.get('razorpay_enabled') == 'on',
        'cod_enabled': request.POST.get('cod_enabled') == 'on',
        'upi_id': request.POST.get('upi_id', ''),
    }
    kv.value = data
    kv.save()
    # Write to .env file if it exists
    import os
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r') as ef:
                lines = ef.readlines()
            keys_to_update = {
                'RAZORPAY_KEY_ID': data['razorpay_key_id'],
                'RAZORPAY_KEY_SECRET': data['razorpay_key_secret'],
            }
            updated_keys = set()
            new_lines = []
            for line in lines:
                written = False
                for k, v in keys_to_update.items():
                    if line.startswith(f'{k}='):
                        new_lines.append(f'{k}={v}\n')
                        updated_keys.add(k)
                        written = True
                        break
                if not written:
                    new_lines.append(line)
            for k, v in keys_to_update.items():
                if k not in updated_keys:
                    new_lines.append(f'{k}={v}\n')
            with open(env_path, 'w') as ef:
                ef.writelines(new_lines)
        except Exception:
            pass
    messages.success(request, 'Payment settings saved.')
    return redirect('dashboard:payment_settings')


# ---- Email Settings ----

@admin_required
def email_settings_view(request):
    try:
        kv = KeyValueStore.objects.get(key='email_settings')
        email_data = kv.value
    except KeyValueStore.DoesNotExist:
        from django.conf import settings as django_settings
        email_data = {
            'host': getattr(django_settings, 'EMAIL_HOST', ''),
            'port': getattr(django_settings, 'EMAIL_PORT', 587),
            'user': getattr(django_settings, 'EMAIL_HOST_USER', ''),
            'from_email': getattr(django_settings, 'DEFAULT_FROM_EMAIL', ''),
            'use_tls': True,
        }
    return render(request, 'dashboard/settings/email.html', {'email_data': email_data})


@admin_required
@require_POST
def email_settings_save(request):
    kv, _ = KeyValueStore.objects.get_or_create(key='email_settings')
    data = {
        'host': request.POST.get('host', ''),
        'port': int(request.POST.get('port', 587) or 587),
        'user': request.POST.get('user', ''),
        'password': request.POST.get('password', ''),
        'from_email': request.POST.get('from_email', ''),
        'use_tls': request.POST.get('use_tls') == 'on',
    }
    kv.value = data
    kv.save()
    messages.success(request, 'Email settings saved.')
    return redirect('dashboard:email_settings')


# ---- Menus ----

@admin_required
def menus_view(request):
    menus = Menu.objects.all()
    selected_id = request.GET.get('menu')
    selected = None
    if selected_id:
        try:
            selected = Menu.objects.get(id=selected_id)
        except Menu.DoesNotExist:
            pass
    if not selected and menus.exists():
        selected = menus.first()
    return render(request, 'dashboard/menus/menus.html', {
        'menus': menus, 'selected': selected,
    })


@admin_required
@require_POST
def menus_save(request):
    menu_id = request.POST.get('menu_id')
    action = request.POST.get('action', 'save')

    if action == 'create':
        from store.models import generate_id
        name = request.POST.get('name', 'New Menu')
        m = Menu.objects.create(id=generate_id(), name=name, items=[])
        messages.success(request, f'Menu "{name}" created.')
        return redirect(f"{request.path}?menu={m.id}")

    if action == 'delete' and menu_id:
        Menu.objects.filter(id=menu_id).delete()
        messages.success(request, 'Menu deleted.')
        return redirect('dashboard:menus')

    if menu_id:
        menu = get_object_or_404(Menu, id=menu_id)
        menu.name = request.POST.get('name', menu.name)
        try:
            menu.items = json.loads(request.POST.get('items_json', '[]'))
        except Exception:
            pass
        menu.save()
        messages.success(request, 'Menu saved.')
        return redirect(f"{request.path}?menu={menu_id}")

    return redirect('dashboard:menus')


# ---- Minimalist Homepage Visual Editor ----

MINIMALIST_SECTIONS = [
    ('hero', 'Hero Slider'),
    ('diamond_interpretations', 'Diamond Interpretations'),
    ('signature_collections', 'Signature Collections'),
    ('category_grid_with_trending', 'Category Grid & Trending'),
    ('newestProducts', 'Newest Products'),
    ('world_of_brand', 'World of Brand'),
    ('bestSellers', 'Best Sellers'),
    ('imageSlider', 'Image Slider'),
    ('splitBanner', 'Split Banner'),
    ('textHighlights', 'Text Highlights'),
    ('imageGrid', 'Image Grid'),
    ('instagram', 'Instagram'),
    ('testimonials', 'Testimonials'),
    ('assurance_and_exchange', 'Assurance & Exchange'),
    ('journal', 'Journal'),
    ('gifts_and_experiences', 'Gifts & Experiences'),
]


@admin_required
def minimalist_editor_view(request):
    try:
        kv = KeyValueStore.objects.get(key='minimalist_homepage_content')
        content = kv.value
    except KeyValueStore.DoesNotExist:
        content = {}
    categories = list(Category.objects.filter(is_active=True).values('id', 'name'))
    return render(request, 'dashboard/appearance/minimalist_editor.html', {
        'content': content,
        'content_json': json.dumps(content, indent=2),
        'categories': categories,
        'sections': MINIMALIST_SECTIONS,
    })


@admin_required
@require_POST
def minimalist_editor_save(request):
    kv, _ = KeyValueStore.objects.get_or_create(key='minimalist_homepage_content')
    section = request.POST.get('section')

    try:
        current = kv.value or {}
    except Exception:
        current = {}

    if section:
        # Partial section save from visual editor
        try:
            section_data = json.loads(request.POST.get('section_data', '{}'))
            current[section] = section_data
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        # Full JSON save
        try:
            current = json.loads(request.POST.get('content_json', '{}'))
        except Exception as e:
            messages.error(request, f'Invalid JSON: {e}')
            return redirect('dashboard:minimalist_editor')

    kv.value = current
    kv.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or section:
        return JsonResponse({'success': True})
    clear_store_cache()
    messages.success(request, 'Minimalist content saved.')
    return redirect('dashboard:minimalist_editor')
