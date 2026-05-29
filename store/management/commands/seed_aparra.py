import json
from django.core.management.base import BaseCommand
from store.models import Category, KeyValueStore


class Command(BaseCommand):
    help = 'Seed categories, menu, theme settings, and homepage content from the original Aparra data'

    def handle(self, *args, **options):
        self.seed_categories()
        self.seed_theme_settings()
        self.seed_minimalist_content()
        self.seed_footer_content()
        self.seed_site_settings()
        self.stdout.write(self.style.SUCCESS('All Aparra data seeded successfully.'))

    # ─── Categories ────────────────────────────────────────────────────────────

    def seed_categories(self):
        top_level = [
            ('cat-rings',           'Rings',                0),
            ('cat-earrings',        'Ear rings',            1),
            ('cat-necklace-pendants','Necklace & Pendants', 2),
            ('cat-wedding',         'Wedding',              3),
            ('cat-bracelets-bangles','Bracelets and Bangles',4),
            ('cat-mangalsutra',     'Mangalsutra',          5),
            ('cat-gifting',         'Gifting',              6),
            ('cat-budget',          'Shop on Budget',       7),
        ]
        for cat_id, name, order in top_level:
            Category.objects.update_or_create(
                id=cat_id,
                defaults={'name': name, 'sort_order': order, 'is_active': True, 'parent': None},
            )

        sub_categories = [
            # Rings
            ('cat-rings-everyday',   'Everyday',                 'cat-rings', 0),
            ('cat-rings-gold',       'Gold Rings',               'cat-rings', 1),
            ('cat-rings-diamond',    'Diamond Stacks',           'cat-rings', 2),
            ('cat-rings-engagement', 'Engagement',               'cat-rings', 3),
            ('cat-rings-couple',     'Couple ring',              'cat-rings', 4),
            ('cat-rings-cocktail',   'Cocktail',                 'cat-rings', 5),
            ('cat-rings-mens',       "Men's Signature Bands",    'cat-rings', 6),
            # Earrings
            ('cat-earrings-studs',    'Studs',     'cat-earrings', 0),
            ('cat-earrings-hoops',    'Hoops',     'cat-earrings', 1),
            ('cat-earrings-danglers', 'Danglers',  'cat-earrings', 2),
            # Necklace & Pendants
            ('cat-necklace-choker',      'Choker',         'cat-necklace-pendants', 0),
            ('cat-necklace-chain',       'Chain Pendants', 'cat-necklace-pendants', 1),
            ('cat-necklace-mangalsutra', 'Mangalsutra',    'cat-necklace-pendants', 2),
            ('cat-necklace-solitaire',   'Solitaire',      'cat-necklace-pendants', 3),
            # Wedding
            ('cat-wedding-rings',       'Rings',                        'cat-wedding', 0),
            ('cat-wedding-sets',        'Sets',                         'cat-wedding', 1),
            ('cat-wedding-mangalsutra', 'Core Collection Mangalsutra',  'cat-wedding', 2),
            # Bracelets and Bangles
            ('cat-bracelets-diamond',    'Diamond Bracelets',    'cat-bracelets-bangles', 0),
            ('cat-bracelets-tennis',     'Tennis Bracelets',     'cat-bracelets-bangles', 1),
            ('cat-bracelets-gold',       'Gold Bangles',         'cat-bracelets-bangles', 2),
            ('cat-bracelets-adjustable', 'Adjustable Bracelets', 'cat-bracelets-bangles', 3),
            # Mangalsutra
            ('cat-mangalsutra-modern',      'Modern',                'cat-mangalsutra', 0),
            ('cat-mangalsutra-traditional', 'Traditional',           'cat-mangalsutra', 1),
            ('cat-mangalsutra-solitaire',   'Solitaire',             'cat-mangalsutra', 2),
            ('cat-mangalsutra-bracelets',   'Mangalsutra Bracelets', 'cat-mangalsutra', 3),
            # Gifting
            ('cat-gifting-anniversary',  'Anniversary',  'cat-gifting', 0),
            ('cat-gifting-personalised', 'Personalised', 'cat-gifting', 1),
            ('cat-gifting-self',         'Self Gift',    'cat-gifting', 2),
            ('cat-gifting-him',          'For Him',      'cat-gifting', 3),
            ('cat-gifting-her',          'For Her',      'cat-gifting', 4),
            ('cat-gifting-father',       'For Father',   'cat-gifting', 5),
            ('cat-gifting-kids',         'For Kids',     'cat-gifting', 6),
            # Shop on Budget
            ('cat-budget-under20', 'Under 20k',  'cat-budget', 0),
            ('cat-budget-under30', 'Under 30k',  'cat-budget', 1),
            ('cat-budget-under40', 'Under 40k',  'cat-budget', 2),
            ('cat-budget-under50', 'Under 50k',  'cat-budget', 3),
            ('cat-budget-above50', 'Above 50k',  'cat-budget', 4),
        ]
        for cat_id, name, parent_id, order in sub_categories:
            parent = Category.objects.get(id=parent_id)
            Category.objects.update_or_create(
                id=cat_id,
                defaults={'name': name, 'sort_order': order, 'is_active': True, 'parent': parent},
            )
        self.stdout.write('  Categories seeded.')

    # ─── Theme settings ────────────────────────────────────────────────────────

    def seed_theme_settings(self):
        KeyValueStore.objects.update_or_create(
            key='theme_settings',
            defaults={'value': {'activeHomepageTheme': 'minimalist', 'activeProductTheme': 'default'}},
        )
        self.stdout.write('  Theme settings seeded.')

    # ─── Minimalist homepage content ───────────────────────────────────────────

    def seed_minimalist_content(self):
        content = {
            "hero": {
                "enabled": True,
                "slides": [
                    {
                        "id": "slide-1",
                        "type": "image",
                        "title": "Modern Interpretations in Diamonds",
                        "subtitle": "Crafted for today, inspired by heritage.",
                        "cta": {"label": "Explore Collection", "href": "/shop/"},
                        "imageUrl": "https://images.unsplash.com/photo-1602107536707-a4a8111d3151?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                        "videoUrl": ""
                    },
                    {
                        "id": "slide-2",
                        "type": "video",
                        "title": "Experience the Movement",
                        "subtitle": "Our jewelry in motion, bringing each piece to life.",
                        "cta": {"label": "Shop Now", "href": "/shop/"},
                        "imageUrl": "https://images.unsplash.com/photo-1588444968576-f7b99076a7e5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                        "videoUrl": "https://cdn.pixabay.com/video/2018/11/10/19253-300109077_large.mp4"
                    }
                ]
            },
            "diamond_interpretations": {
                "enabled": True,
                "title": "",
                "cards": [
                    {"id": "earrings", "title": "Earrings", "image": "https://images.unsplash.com/photo-1761479258392-011cb2090063?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-earrings/"},
                    {"id": "necklaces", "title": "Necklaces", "image": "https://images.unsplash.com/photo-1611012844392-f4f96c7fd052?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-necklace-pendants/"},
                    {"id": "rings", "title": "Rings", "image": "https://images.unsplash.com/photo-1611955167811-4711904bb9f8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-rings/"}
                ]
            },
            "signature_collections": {
                "enabled": True,
                "title": "",
                "collections": {
                    "primary": {
                        "id": "primary-collection",
                        "title": "Floral Bloom",
                        "image": "https://images.unsplash.com/photo-1631050165155-421c47e306f7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                        "href": "/shop/",
                        "type": "image",
                        "videoUrl": None
                    },
                    "secondary": [
                        {"id": "earrings", "title": "Stunning Earrings", "image": "https://images.unsplash.com/photo-1762344352608-7b85a0834904?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-earrings/"},
                        {"id": "wedding", "title": "Wedding Gifts", "image": "https://images.unsplash.com/photo-1525350109470-a8c4ff3d3aae?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-wedding/"}
                    ]
                }
            },
            "category_grid_with_trending": {
                "enabled": True,
                "categories": {
                    "title": "",
                    "items": [
                        {"id": "gold",       "title": "Gold",       "image": "https://images.unsplash.com/photo-1724896732926-cad47e0080a2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-rings-gold/"},
                        {"id": "diamond",    "title": "Diamond",    "image": "https://images.unsplash.com/photo-1731657017065-6bf400d479fd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-rings-diamond/"},
                        {"id": "earrings",   "title": "Earrings",   "image": "https://images.unsplash.com/photo-1643822523123-241d959fa1d5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-earrings/"},
                        {"id": "pendants",   "title": "Pendants",   "image": "https://images.unsplash.com/photo-1664178266066-e37e0d25e6a1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-necklace-pendants/"},
                        {"id": "bracelets",  "title": "Bracelets",  "image": "https://images.unsplash.com/photo-1758995116383-f51775896add?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-bracelets-bangles/"},
                        {"id": "dailywear",  "title": "Dailywear",  "image": "https://images.unsplash.com/photo-1708221269898-27fc12754dfc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-rings-everyday/"}
                    ]
                },
                "trending": {
                    "title": "",
                    "items": [
                        {"id": "trend-1", "title": "Elegant Diamond Ring",    "image": "https://images.unsplash.com/photo-1595538934869-503c9448981b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/shop/"},
                        {"id": "trend-2", "title": "Classic Gold Necklace",   "image": "https://images.unsplash.com/photo-1671663906664-9586041c3aa1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/shop/"},
                        {"id": "trend-3", "title": "Modern Stud Earrings",    "image": "https://images.unsplash.com/photo-1584948221378-93841f589fb7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/shop/"}
                    ]
                }
            },
            "newestProducts": {"enabled": True, "title": "New Arrivals", "categoryId": None},
            "world_of_brand": {
                "enabled": True,
                "title": "World of Aparra",
                "items": [
                    {"id": "wedding", "title": "Wedding",  "image": "https://images.unsplash.com/photo-1525350109470-a8c4ff3d3aae?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-wedding/"},
                    {"id": "diamond", "title": "Diamond",  "image": "https://images.unsplash.com/photo-1731657017065-6bf400d479fd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "href": "/category/cat-rings-diamond/"}
                ]
            },
            "bestSellers": {"enabled": True, "title": "Best Sellers", "categoryId": None},
            "imageSlider": {
                "enabled": True,
                "eyebrow": "Styled for You",
                "title": "In the Spotlight",
                "ctaText": "Shop the Look",
                "ctaLink": "/shop/",
                "items": [
                    {"id": "look1", "imageUrl": "https://images.unsplash.com/photo-1620912189836-121658428a34?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "model wearing necklace", "link": "/shop/"},
                    {"id": "look2", "imageUrl": "https://images.unsplash.com/photo-1617059322001-a61ce9551e08?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "model wearing earrings", "link": "/shop/"},
                    {"id": "look3", "imageUrl": "https://images.unsplash.com/photo-1611312338608-7245995a4321?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "model with jewelry", "link": "/shop/"},
                    {"id": "look4", "imageUrl": "https://images.unsplash.com/photo-1631050165155-421c47e306f7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "close up jewelry", "link": "/shop/"},
                    {"id": "look5", "imageUrl": "https://images.unsplash.com/photo-1602107536707-a4a8111d3151?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "lifestyle with jewelry", "link": "/shop/"}
                ]
            },
            "splitBanner": {
                "enabled": True,
                "banners": [
                    {"id": "banner-1", "title": "For Everyday Elegance", "description": "Discover pieces that shine with you, every single day.", "buttonLabel": "Shop Dailywear", "buttonLink": "/category/cat-rings-everyday/", "imageUrl": "https://images.unsplash.com/photo-1602107536707-a4a8111d3151?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "lifestyle fashion"},
                    {"id": "banner-2", "title": "The Art of Gifting",    "description": "Find the perfect present for every occasion and everyone on your list.", "buttonLabel": "Explore Gifts", "buttonLink": "/category/cat-gifting/", "imageUrl": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "gift box"}
                ]
            },
            "textHighlights": {
                "enabled": True,
                "items": [
                    {"id": "h1", "title": "Free Shipping",      "description": "On all orders across India"},
                    {"id": "h2", "title": "15-Day Returns",     "description": "No questions asked"},
                    {"id": "h3", "title": "Certified Jewellery","description": "BIS Hallmark & GIA/IGI"},
                    {"id": "h4", "title": "Lifetime Warranty",  "description": "For your peace of mind"}
                ]
            },
            "imageGrid": {
                "enabled": True,
                "items": [
                    {"id": "g1", "type": "image", "imageUrl": "https://images.unsplash.com/photo-1631050165155-421c47e306f7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "jewelry detail"},
                    {"id": "g2", "type": "text",  "title": "Our Philosophy", "content": "To create timeless pieces that are cherished for generations.", "buttonLabel": "Learn More", "buttonLink": "/shop/"},
                    {"id": "g3", "type": "image", "imageUrl": "https://images.unsplash.com/photo-1617059322001-a61ce9551e08?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "model portrait"},
                    {"id": "g4", "type": "image", "imageUrl": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80", "imageHint": "abstract texture"}
                ]
            },
            "instagram": {
                "enabled": True,
                "handle": "@aparra_jewels",
                "postImageUrls": [
                    "https://images.unsplash.com/photo-1599351433895-0ab8c0e21544?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                    "https://images.unsplash.com/photo-1605100804763-247f67b3557e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                    "https://images.unsplash.com/photo-1619119069152-4a04595c5c4a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                    "https://images.unsplash.com/photo-1610216654532-6a78a6a6e7c8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80"
                ]
            },
            "testimonials": {
                "enabled": True,
                "title": "What Our Customers Say",
                "items": [
                    {"id": "1", "name": "Priya S.",   "location": "Mumbai",    "text": "The ring I bought is absolutely stunning! The craftsmanship is top-notch, and it feels so special.", "rating": 5, "imageUrl": "https://images.unsplash.com/photo-1646206532396-a1d6b79a7731?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=80&q=80", "imageHint": "happy woman"},
                    {"id": "2", "name": "Rohan K.",   "location": "Delhi",     "text": "I purchased a gift for my wife, and she was thrilled. The packaging was as beautiful as the necklace inside.", "rating": 5, "imageUrl": "https://images.unsplash.com/photo-1668804985095-0e6c33f99fb9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=80&q=80", "imageHint": "smiling man"},
                    {"id": "3", "name": "Ananya M.",  "location": "Bangalore", "text": "From the customer service to the product itself, my experience was seamless. The everyday diamonds are perfect for my style.", "rating": 5, "imageUrl": "https://images.unsplash.com/photo-1763385128836-053af3c6a91f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=80&q=80", "imageHint": "elegant woman"}
                ]
            },
            "assurance_and_exchange": {
                "enabled": True,
                "assurance": {
                    "title": "Our Assurance",
                    "items": [
                        {"id": "certified", "title": "Certified Jewellery",   "description": "Authenticity guaranteed with certified purity and quality.", "icon": "award"},
                        {"id": "lifetime",  "title": "Lifetime Maintenance",  "description": "Free lifetime cleaning and inspection.",                     "icon": "wrench"},
                        {"id": "returns",   "title": "Easy Returns",           "description": "Hassle-free returns and exchanges.",                         "icon": "replace"}
                    ]
                },
                "exchange": {
                    "title": "Exchange Your Old Gold",
                    "subtitle": "Upgrade your jewellery with our transparent exchange program.",
                    "image": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                    "cta": {"label": "Know More", "href": "/shop/"}
                }
            },
            "journal": {"enabled": True, "title": "From Our Journal", "categoryId": None},
            "gifts_and_experiences": {
                "enabled": True,
                "gift": {
                    "title": "The Perfect Gift",
                    "subtitle": "Celebrate moments with jewellery that lasts forever.",
                    "image": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080&q=80",
                    "cta": {"label": "Explore Gifts", "href": "/category/cat-gifting/"}
                },
                "experiences": {
                    "title": "Jewellery Experiences",
                    "items": [
                        {"id": "digital-gold",   "title": "Digital Gold",          "subtitle": "Invest in gold securely online.",         "image": "https://images.unsplash.com/photo-1758995116383-f51775896add?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400&q=80", "href": "/shop/"},
                        {"id": "appointment",    "title": "Book an Appointment",   "subtitle": "Personalized in-store experience.",       "image": "https://images.unsplash.com/photo-1562682524-3136f32e0a74?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400&q=80", "href": "/shop/"},
                        {"id": "jewellery-care", "title": "Jewellery Care",        "subtitle": "Keep your jewellery shining forever.",    "image": "https://images.unsplash.com/photo-1745542284155-52a2d488547b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400&q=80", "href": "/shop/"}
                    ]
                }
            }
        }
        KeyValueStore.objects.update_or_create(
            key='minimalist_homepage_content',
            defaults={'value': content},
        )
        self.stdout.write('  Minimalist content seeded.')

    # ─── Footer content ────────────────────────────────────────────────────────

    def seed_footer_content(self):
        footer = {
            "columns": [
                {
                    "id": "col1", "title": "Useful Links",
                    "links": [
                        {"id": "l1-1", "label": "Track your Order", "url": "#"},
                        {"id": "l1-2", "label": "Returns",           "url": "#"},
                        {"id": "l1-3", "label": "Shipments",         "url": "#"},
                        {"id": "l1-4", "label": "Encircle Program",  "url": "#"},
                        {"id": "l1-5", "label": "Find a Store",      "url": "#"}
                    ]
                },
                {
                    "id": "col2", "title": "Information",
                    "links": [
                        {"id": "l2-1", "label": "Gemstone Guide",  "url": "#"},
                        {"id": "l2-2", "label": "Metal Guide",     "url": "#"},
                        {"id": "l2-3", "label": "Diamond Guide",   "url": "#"},
                        {"id": "l2-4", "label": "About Aparra",    "url": "#"}
                    ]
                }
            ],
            "contact": {"email": "support@aparra.com"},
            "locations": [
                {"id": "loc1", "name": "UAE"},
                {"id": "loc2", "name": "Singapore"},
                {"id": "loc3", "name": "Qatar"},
                {"id": "loc4", "name": "Oman"}
            ],
            "socials": {
                "facebook": "#",
                "instagram": "#",
                "twitter": "#",
                "youtube": "#"
            },
            "bottom": {
                "copyright": "© 2026 Aparra. All rights reserved.",
                "links": [
                    {"id": "b1", "label": "Terms & Conditions", "url": "#"},
                    {"id": "b2", "label": "Privacy Notice",     "url": "#"}
                ]
            }
        }
        KeyValueStore.objects.update_or_create(
            key='footer_content',
            defaults={'value': footer},
        )
        self.stdout.write('  Footer content seeded.')

    # ─── Site settings (menu) ──────────────────────────────────────────────────

    def seed_site_settings(self):
        menu_items = [
            {
                "label": "Rings", "link": "/category/cat-rings/",
                "children": [
                    {"label": "Everyday",             "link": "/category/cat-rings-everyday/"},
                    {"label": "Gold Rings",            "link": "/category/cat-rings-gold/"},
                    {"label": "Diamond Stacks",        "link": "/category/cat-rings-diamond/"},
                    {"label": "Engagement",            "link": "/category/cat-rings-engagement/"},
                    {"label": "Couple ring",           "link": "/category/cat-rings-couple/"},
                    {"label": "Cocktail",              "link": "/category/cat-rings-cocktail/"},
                    {"label": "Men's Signature Bands", "link": "/category/cat-rings-mens/"}
                ],
                "promoTitle": "Featured Rings",
                "promoImageUrl": "https://picsum.photos/seed/promo-rings/400/500",
                "promoLink": "/category/cat-rings/",
                "promo2Title": "Couple Bands",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-couple/400/500",
                "promo2Link": "/category/cat-rings-couple/"
            },
            {
                "label": "Ear rings", "link": "/category/cat-earrings/",
                "children": [
                    {"label": "Studs",    "link": "/category/cat-earrings-studs/"},
                    {"label": "Hoops",    "link": "/category/cat-earrings-hoops/"},
                    {"label": "Danglers", "link": "/category/cat-earrings-danglers/"}
                ],
                "promoTitle": "Stunning Earrings",
                "promoImageUrl": "https://picsum.photos/seed/promo-earrings/400/500",
                "promoLink": "/category/cat-earrings-studs/",
                "promo2Title": "Hoops for Days",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-hoops/400/500",
                "promo2Link": "/category/cat-earrings-hoops/"
            },
            {
                "label": "Necklace & Pendants", "link": "/category/cat-necklace-pendants/",
                "children": [
                    {"label": "Choker",      "link": "/category/cat-necklace-choker/"},
                    {"label": "Chain Pendants","link": "/category/cat-necklace-chain/"},
                    {"label": "Mangalsutra", "link": "/category/cat-necklace-mangalsutra/"},
                    {"label": "Solitaire",   "link": "/category/cat-necklace-solitaire/"}
                ],
                "promoTitle": "Layering Necklaces",
                "promoImageUrl": "https://picsum.photos/seed/promo-necklaces/400/500",
                "promoLink": "/category/cat-necklace-pendants/",
                "promo2Title": "Solitaire Pendants",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-solitaire/400/500",
                "promo2Link": "/category/cat-necklace-solitaire/"
            },
            {
                "label": "Wedding", "link": "/category/cat-wedding/",
                "children": [
                    {"label": "Rings",                        "link": "/category/cat-wedding-rings/"},
                    {"label": "Sets",                         "link": "/category/cat-wedding-sets/"},
                    {"label": "Core Collection Mangalsutra",  "link": "/category/cat-wedding-mangalsutra/"}
                ],
                "promoTitle": "Bridal Sets",
                "promoImageUrl": "https://picsum.photos/seed/promo-wedding/400/500",
                "promoLink": "/category/cat-wedding-sets/",
                "promo2Title": "Wedding Bands",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-bands/400/500",
                "promo2Link": "/category/cat-wedding-rings/"
            },
            {
                "label": "Bracelets and Bangles", "link": "/category/cat-bracelets-bangles/",
                "children": [
                    {"label": "Diamond Bracelets",    "link": "/category/cat-bracelets-diamond/"},
                    {"label": "Tennis Bracelets",     "link": "/category/cat-bracelets-tennis/"},
                    {"label": "Gold Bangles",         "link": "/category/cat-bracelets-gold/"},
                    {"label": "Adjustable Bracelets", "link": "/category/cat-bracelets-adjustable/"}
                ],
                "promoTitle": "Arm Candy",
                "promoImageUrl": "https://picsum.photos/seed/promo-bracelets/400/500",
                "promoLink": "/category/cat-bracelets-bangles/",
                "promo2Title": "Tennis Bracelets",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-tennis/400/500",
                "promo2Link": "/category/cat-bracelets-tennis/"
            },
            {
                "label": "Mangalsutra", "link": "/category/cat-mangalsutra/",
                "children": [
                    {"label": "Modern",                "link": "/category/cat-mangalsutra-modern/"},
                    {"label": "Traditional",           "link": "/category/cat-mangalsutra-traditional/"},
                    {"label": "Solitaire",             "link": "/category/cat-mangalsutra-solitaire/"},
                    {"label": "Mangalsutra Bracelets", "link": "/category/cat-mangalsutra-bracelets/"}
                ],
                "promoTitle": "Modern Mangalsutra",
                "promoImageUrl": "https://picsum.photos/seed/promo-mangal/400/500",
                "promoLink": "/category/cat-mangalsutra-modern/",
                "promo2Title": "Bracelet Style",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-mangal-bracelet/400/500",
                "promo2Link": "/category/cat-mangalsutra-bracelets/"
            },
            {
                "label": "Gifting", "link": "/category/cat-gifting/",
                "children": [
                    {"label": "Anniversary",  "link": "/category/cat-gifting-anniversary/"},
                    {"label": "Personalised", "link": "/category/cat-gifting-personalised/"},
                    {"label": "Self Gift",    "link": "/category/cat-gifting-self/"},
                    {"label": "For Him",      "link": "/category/cat-gifting-him/"},
                    {"label": "For Her",      "link": "/category/cat-gifting-her/"},
                    {"label": "For Father",   "link": "/category/cat-gifting-father/"},
                    {"label": "For Kids",     "link": "/category/cat-gifting-kids/"}
                ],
                "promoTitle": "Perfect Gifts",
                "promoImageUrl": "https://picsum.photos/seed/promo-gifting/400/500",
                "promoLink": "/category/cat-gifting/",
                "promo2Title": "Personalized Gifts",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-personal/400/500",
                "promo2Link": "/category/cat-gifting-personalised/"
            },
            {
                "label": "Shop on Budget", "link": "/category/cat-budget/",
                "children": [
                    {"label": "Under 20k", "link": "/category/cat-budget-under20/"},
                    {"label": "Under 30k", "link": "/category/cat-budget-under30/"},
                    {"label": "Under 40k", "link": "/category/cat-budget-under40/"},
                    {"label": "Under 50k", "link": "/category/cat-budget-under50/"},
                    {"label": "Above 50k", "link": "/category/cat-budget-above50/"}
                ],
                "promoTitle": "Affordable Luxury",
                "promoImageUrl": "https://picsum.photos/seed/promo-budget/400/500",
                "promoLink": "/category/cat-budget/",
                "promo2Title": "Under 20k",
                "promo2ImageUrl": "https://picsum.photos/seed/promo-under20k/400/500",
                "promo2Link": "/category/cat-budget-under20/"
            }
        ]

        kv, _ = KeyValueStore.objects.get_or_create(key='settings', defaults={'value': {}})
        settings_val = kv.value or {}
        settings_val['menu_items'] = menu_items
        if 'whatsapp' not in settings_val:
            settings_val['whatsapp'] = {
                'enabled': True,
                'phoneNumber': '9266030700',
                'defaultMessage': 'Hello! I saw your store and I am interested in your products.'
            }
        kv.value = settings_val
        kv.save()
        self.stdout.write('  Site settings (menu) seeded.')
