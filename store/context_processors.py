from .models import KeyValueStore, Category
from .cart import Cart


def cart_processor(request):
    cart = Cart(request)
    return {'cart': cart, 'cart_count': len(cart)}


def site_settings_processor(request):
    try:
        kv = KeyValueStore.objects.get(key='settings')
        settings = kv.value
    except KeyValueStore.DoesNotExist:
        settings = {}
    return {
        'site_settings': settings,
        'whatsapp_enabled': settings.get('whatsapp', {}).get('enabled', False),
        'whatsapp_number': settings.get('whatsapp', {}).get('phoneNumber', ''),
        'whatsapp_message': settings.get('whatsapp', {}).get('defaultMessage', ''),
    }


def nav_categories_processor(request):
    top_level = Category.objects.filter(is_active=True, parent=None).order_by('sort_order', 'name')
    nav_cats = []
    for cat in top_level:
        nav_cats.append({
            'id': cat.id,
            'name': cat.name,
            'image_url': cat.image_url,
            'children': list(cat.children.filter(is_active=True).order_by('sort_order', 'name').values('id', 'name', 'image_url')),
        })
    return {'nav_categories': nav_cats}
