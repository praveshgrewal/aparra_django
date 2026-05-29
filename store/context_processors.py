from .models import KeyValueStore, Category
from .cart import Cart
from django.core.cache import cache

CACHE_TTL = 300  # 5 minutes


def cart_processor(request):
    cart = Cart(request)
    return {'cart': cart, 'cart_count': len(cart)}


def site_settings_processor(request):
    settings = cache.get('site_settings')
    if settings is None:
        try:
            kv = KeyValueStore.objects.get(key='site_settings')
            settings = kv.value
        except KeyValueStore.DoesNotExist:
            try:
                kv = KeyValueStore.objects.get(key='settings')
                settings = kv.value
            except KeyValueStore.DoesNotExist:
                settings = {}
        cache.set('site_settings', settings, CACHE_TTL)
    return {
        'site_settings': settings,
        'whatsapp_enabled': settings.get('whatsapp', {}).get('enabled', False),
        'whatsapp_number': settings.get('whatsapp', {}).get('phoneNumber', ''),
        'whatsapp_message': settings.get('whatsapp', {}).get('defaultMessage', ''),
    }


def nav_categories_processor(request):
    nav_cats = cache.get('nav_categories')
    if nav_cats is None:
        top_level = Category.objects.filter(
            is_active=True, parent=None
        ).prefetch_related('children').order_by('sort_order', 'name')

        nav_cats = []
        for cat in top_level:
            nav_cats.append({
                'id': cat.id,
                'name': cat.name,
                'image_url': cat.image_url,
                'children': list(
                    cat.children.filter(is_active=True)
                    .order_by('sort_order', 'name')
                    .values('id', 'name', 'image_url')
                ),
            })
        cache.set('nav_categories', nav_cats, CACHE_TTL)
    return {'nav_categories': nav_cats}
