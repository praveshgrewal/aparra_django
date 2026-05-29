"""
Management command to seed sample data matching the original Next.js Aparra website.
Run: python manage.py seed_data
"""
import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Metal, Purity, TaxClass, Product, KeyValueStore


HOMEPAGE_CONTENT = {
  "layout": [
    {"id": "hero", "type": "hero", "visible": True},
    {"id": "iconHighlights", "type": "iconHighlights", "visible": True},
    {"id": "heroSlider", "type": "heroSlider", "visible": True},
    {"id": "videoHighlights", "type": "videoHighlights", "visible": True},
    {"id": "newestProducts", "type": "newestProducts", "visible": True},
    {"id": "promoBanners", "type": "promoBanners", "visible": True},
    {"id": "imageBanner1", "type": "imageBanner1", "visible": True},
    {"id": "shopByCategory", "type": "shopByCategory", "visible": True},
    {"id": "bestSellers", "type": "bestSellers", "visible": True},
    {"id": "imageBanner2", "type": "imageBanner2", "visible": True},
    {"id": "testimonials", "type": "testimonials", "visible": True},
    {"id": "journal", "type": "journal", "visible": True},
  ],
  "isEnabled": True,
  "hero": {
    "title": "At Aparra We Care About",
    "titleHighlight": "YOU",
    "subtitle": "We believe that jewelry is passed to coming generations.",
    "ctaText": "Buy Now",
    "ctaLink": "/shop/",
    "videoUrl": "https://www.youtube.com/watch?v=R6NOFwT8JtM",
    "fallbackImageUrl": "https://images.unsplash.com/photo-1756355201570-4437a6e34717?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    "videoEnabled": True,
    "videoStartTime": 10,
    "videoEndTime": 0
  },
  "iconHighlights": {
    "items": [
      {"id": "rings", "label": "Rings", "link": "/shop/?q=ring", "imageUrl": "https://images.unsplash.com/photo-1611955167811-4711904bb9f8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
      {"id": "earrings", "label": "Earrings", "link": "/shop/?q=earring", "imageUrl": "https://images.unsplash.com/photo-1685489807405-fdffb06aef2c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
      {"id": "necklaces", "label": "Necklaces", "link": "/shop/?q=necklace", "imageUrl": "https://images.unsplash.com/photo-1671663906664-9586041c3aa1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
      {"id": "bracelets", "label": "Bracelets", "link": "/shop/?q=bracelet", "imageUrl": "https://images.unsplash.com/photo-1679156271456-d6068c543ee7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
      {"id": "gifting", "label": "Gifting", "link": "/shop/", "imageUrl": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    ]
  },
  "heroSlider": {
    "items": [
      {
        "id": "slide1",
        "title": "Vintage 18K Gold Bracelets",
        "subtitle": "Elegance isn't solely defined by what you wear. It's how you carry yourself, how you speak, what you read.",
        "ctaText": "Shop Now",
        "ctaLink": "/shop/",
        "imageUrl": "https://images.unsplash.com/photo-1758995116383-f51775896add?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
        "imageHint": "gold bangles stack"
      },
      {
        "id": "slide2",
        "title": "Timeless Diamond Collection",
        "subtitle": "Discover brilliance that lasts a lifetime. Our diamonds are ethically sourced and masterfully cut.",
        "ctaText": "Explore Diamonds",
        "ctaLink": "/shop/",
        "imageUrl": "https://images.unsplash.com/photo-1585506172580-9564a524231f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
        "imageHint": "diamond necklace"
      },
      {
        "id": "slide3",
        "title": "Luxury Collection",
        "subtitle": "Discover Luxury that is Dream a lifetime. ethically sourced and masterfully cut.",
        "ctaText": "Explore Collection",
        "ctaLink": "/shop/",
        "imageUrl": "https://images.unsplash.com/photo-1585960622850-ed33c41d6418?fm=jpg&q=80&w=1080",
        "imageHint": "close up of diamond ring"
      }
    ]
  },
  "newestProducts": {"title": "Newest In"},
  "bestSellers": {"title": "Best Sellers"},
  "imageBanner1": {
    "title": "Everyday Diamonds",
    "subtitle": "YOUR DAILY DOSE OF SPARKLE",
    "ctaText": "Shop Now",
    "ctaLink": "/shop/",
    "imageUrl": "https://images.unsplash.com/photo-1673178875233-a1f2e0124b7e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    "imageHint": "woman wearing diamond necklace"
  },
  "imageBanner2": {
    "title": "For the Gifting Season",
    "subtitle": "MAKE MEMORIES WITH APARRA",
    "ctaText": "Explore Gifts",
    "ctaLink": "/shop/",
    "imageUrl": "https://images.unsplash.com/photo-1761479258387-9542d09a5f47?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    "imageHint": "jewelry gift box"
  },
  "shopByCategory": {
    "categories": [
      {"id": "rings", "name": "Rings", "link": "/shop/?q=ring", "imageUrl": "https://images.unsplash.com/photo-1674329109778-0cc72c23537c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "imageHint": "gold diamond ring"},
      {"id": "earrings", "name": "Earrings", "link": "/shop/?q=earring", "imageUrl": "https://images.unsplash.com/photo-1656109801168-699967cf3ba9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "imageHint": "diamond stud earrings"},
      {"id": "necklaces", "name": "Necklaces", "link": "/shop/?q=necklace", "imageUrl": "https://images.unsplash.com/photo-1763256614647-14abbc578252?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "imageHint": "gold pendant necklace"},
      {"id": "bracelets", "name": "Bracelets", "link": "/shop/?q=bracelet", "imageUrl": "https://images.unsplash.com/photo-1663243818736-2b7148eeb2f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "imageHint": "delicate gold bracelet"},
    ]
  },
  "testimonials": {
    "title": "What Our Customers Say",
    "items": [
      {"id": "1", "name": "Priya S.", "location": "Mumbai", "text": "The ring I bought is absolutely stunning! The craftsmanship is top-notch, and it feels so special. I get compliments on it everywhere I go.", "rating": 5, "imageUrl": "https://images.unsplash.com/photo-1646206532396-a1d6b79a7731?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=200"},
      {"id": "2", "name": "Rohan K.", "location": "Delhi", "text": "I purchased a gift for my wife, and she was thrilled. The packaging was as beautiful as the necklace inside. Thank you, Aparra!", "rating": 5, "imageUrl": "https://images.unsplash.com/photo-1668804985095-0e6c33f99fb9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=200"},
      {"id": "3", "name": "Ananya M.", "location": "Bangalore", "text": "From the customer service to the product itself, my experience was seamless. The everyday diamonds are perfect for my style.", "rating": 5, "imageUrl": "https://images.unsplash.com/photo-1763385128836-053af3c6a91f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=200"},
    ]
  },
  "journal": {
    "title": "The Aparra Journal",
    "entries": [
      {"id": "1", "title": "The Art of Layering", "excerpt": "Discover how to masterfully layer your necklaces for a look that's uniquely you.", "link": "/blog/", "imageUrl": "https://images.unsplash.com/photo-1664178266066-e37e0d25e6a1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800"},
      {"id": "2", "title": "A Guide to Wedding Bands", "excerpt": "Find the perfect symbol of your love story with our comprehensive guide to wedding rings.", "link": "/blog/", "imageUrl": "https://images.unsplash.com/photo-1708601421101-9ad139d83f4d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800"},
      {"id": "3", "title": "Caring for Your Treasures", "excerpt": "Keep your fine jewellery sparkling for years to come with our expert care tips.", "link": "/blog/", "imageUrl": "https://images.unsplash.com/photo-1599475704929-b544d0afe078?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800"},
    ]
  },
  "videoHighlights": {
    "eyebrow": "2026 WINTER TRENDS",
    "title": "Check New Trends",
    "description": "Discover our latest collection of handcrafted jewellery, designed for the modern woman who loves timeless elegance.",
    "items": [
      {"id": "vid1", "title": "Engagement Rings", "link": "/shop/?q=ring", "videoUrl": "https://cdn.pixabay.com/video/2025/08/01/294774_large.mp4"},
      {"id": "vid2", "title": "Latest Earrings", "link": "/shop/?q=earring", "videoUrl": "https://cdn.pixabay.com/video/2025/04/08/270861_large.mp4"},
      {"id": "vid3", "title": "Elegant Necklace", "link": "/shop/?q=necklace", "videoUrl": "https://cdn.pixabay.com/video/2025/11/17/316570_large.mp4"},
    ]
  },
  "promoBanners": {
    "items": [
      {"id": "promo1", "title": "New Arrivals", "subtitle": "UPTO 30% OFF", "code": "NEW30", "ctaText": "Shop Now", "ctaLink": "/shop/"},
      {"id": "promo2", "title": "Best Sellers", "subtitle": "UPTO 50% OFF", "code": "BEST50", "ctaText": "Shop Now", "ctaLink": "/shop/"},
    ]
  },
}

FOOTER_CONTENT = {
  "columns": [
    {
      "title": "Collections",
      "links": [
        {"label": "All Jewellery", "url": "/shop/"},
        {"label": "Rings", "url": "/shop/?q=ring"},
        {"label": "Earrings", "url": "/shop/?q=earring"},
        {"label": "Necklaces", "url": "/shop/?q=necklace"},
        {"label": "Bracelets", "url": "/shop/?q=bracelet"},
      ]
    },
    {
      "title": "Customer Care",
      "links": [
        {"label": "Contact Us", "url": "/contact/"},
        {"label": "Track Order", "url": "/accounts/orders/"},
        {"label": "Shipping Policy", "url": "#"},
        {"label": "Returns & Exchange", "url": "#"},
        {"label": "FAQs", "url": "#"},
      ]
    },
    {
      "title": "About",
      "links": [
        {"label": "Our Story", "url": "#"},
        {"label": "Craftsmanship", "url": "#"},
        {"label": "Sustainability", "url": "#"},
        {"label": "Blog", "url": "/blog/"},
      ]
    },
  ],
  "contact": {
    "email": "contact@aparra.com",
  },
  "socials": {
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "youtube": "https://youtube.com",
  },
  "bottom": {
    "copyright": "© 2025 Aparra Jewellery. All rights reserved.",
    "links": [
      {"label": "Privacy Policy", "url": "#"},
      {"label": "Terms", "url": "#"},
    ]
  }
}

SHOP_CONTENT = {
  "hero": {
    "title": "Our Collection",
    "subtitle": "Discover timeless jewellery crafted with passion and precision",
    "imageUrl": "https://images.unsplash.com/photo-1584302179602-e4c3d3fd629d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    "imageHint": "jewellery collection"
  }
}

SITE_SETTINGS = {
  "store": {
    "name": "Aparra Jewellery",
    "email": "contact@aparra.com",
    "phone": "+91 99999 99999",
    "address": "Mumbai, India",
    "currency": "INR",
    "currency_symbol": "₹",
  },
  "whatsapp": {
    "enabled": True,
    "number": "919999999999",
    "message": "Hi, I'm interested in your jewellery collection!",
  }
}

SAMPLE_CATEGORIES = [
    {"name": "Rings", "image_url": "https://images.unsplash.com/photo-1674329109778-0cc72c23537c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    {"name": "Earrings", "image_url": "https://images.unsplash.com/photo-1656109801168-699967cf3ba9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    {"name": "Necklaces", "image_url": "https://images.unsplash.com/photo-1763256614647-14abbc578252?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    {"name": "Bracelets", "image_url": "https://images.unsplash.com/photo-1663243818736-2b7148eeb2f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    {"name": "Pendants", "image_url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    {"name": "Bangles", "image_url": "https://images.unsplash.com/photo-1641562386261-d0c5b9e5bde7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    {"name": "Mangalsutra", "image_url": "https://images.unsplash.com/photo-1591548081688-4ff62d0de286?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
    {"name": "Nose Pins", "image_url": "https://images.unsplash.com/photo-1617038220319-276d3cfab638?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400"},
]

SAMPLE_METALS = [
    {"name": "Gold", "price_per_gram": 6200.0},
    {"name": "Silver", "price_per_gram": 85.0},
    {"name": "Platinum", "price_per_gram": 3200.0},
]

SAMPLE_PURITIES = [
    {"label": "24K", "fineness": 0.999, "metal_name": "Gold"},
    {"label": "22K", "fineness": 0.916, "metal_name": "Gold"},
    {"label": "18K", "fineness": 0.750, "metal_name": "Gold"},
    {"label": "14K", "fineness": 0.585, "metal_name": "Gold"},
    {"label": "925", "fineness": 0.925, "metal_name": "Silver"},
    {"label": "950", "fineness": 0.950, "metal_name": "Platinum"},
]

SAMPLE_PRODUCTS = [
    {
        "name": "22K Gold Mangalsutra with Diamond",
        "description": "A timeless 22K gold mangalsutra featuring delicate diamond detailing. Handcrafted with precision, this piece combines traditional design with modern elegance.",
        "seo_title": "Traditional 22K Gold Mangalsutra",
        "metal_name": "Gold",
        "purity_label": "22K",
        "gross_weight": 12.5,
        "net_weight": 11.2,
        "making_charge_type": "percentage",
        "making_charge_value": 12,
        "category_names": ["Mangalsutra"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1591548081688-4ff62d0de286?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
            {"url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": False},
        ],
        "availability": "in_stock",
        "discount_percentage": 0,
    },
    {
        "name": "18K Diamond Solitaire Ring",
        "description": "An exquisite 18K white gold solitaire ring featuring a brilliant-cut diamond. Perfect for engagements and special occasions.",
        "seo_title": "18K White Gold Diamond Solitaire",
        "metal_name": "Gold",
        "purity_label": "18K",
        "gross_weight": 4.2,
        "net_weight": 3.8,
        "making_charge_type": "percentage",
        "making_charge_value": 15,
        "category_names": ["Rings"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1674329109778-0cc72c23537c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
            {"url": "https://images.unsplash.com/photo-1611955167811-4711904bb9f8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": False},
        ],
        "availability": "in_stock",
        "discount_percentage": 10,
    },
    {
        "name": "22K Gold Jhumka Earrings",
        "description": "Traditional 22K gold jhumka earrings with intricate filigree work. A perfect blend of heritage craftsmanship and contemporary style.",
        "seo_title": "Traditional Gold Jhumka Earrings",
        "metal_name": "Gold",
        "purity_label": "22K",
        "gross_weight": 8.5,
        "net_weight": 7.8,
        "making_charge_type": "percentage",
        "making_charge_value": 14,
        "category_names": ["Earrings"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1656109801168-699967cf3ba9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
            {"url": "https://images.unsplash.com/photo-1685489807405-fdffb06aef2c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": False},
        ],
        "availability": "in_stock",
        "discount_percentage": 0,
    },
    {
        "name": "18K Gold Diamond Pendant Necklace",
        "description": "A stunning 18K gold pendant necklace featuring a brilliant diamond centerpiece. Comes with a delicate 18-inch gold chain.",
        "seo_title": "18K Diamond Pendant Necklace",
        "metal_name": "Gold",
        "purity_label": "18K",
        "gross_weight": 6.8,
        "net_weight": 6.1,
        "making_charge_type": "percentage",
        "making_charge_value": 16,
        "category_names": ["Necklaces", "Pendants"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1763256614647-14abbc578252?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
            {"url": "https://images.unsplash.com/photo-1671663906664-9586041c3aa1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": False},
        ],
        "availability": "in_stock",
        "discount_percentage": 5,
    },
    {
        "name": "22K Gold Kada Bangle",
        "description": "A bold 22K gold kada bangle with traditional engravings. Handcrafted by skilled artisans to represent strength and beauty.",
        "seo_title": "22K Gold Kada Bangle",
        "metal_name": "Gold",
        "purity_label": "22K",
        "gross_weight": 28.0,
        "net_weight": 26.5,
        "making_charge_type": "percentage",
        "making_charge_value": 10,
        "category_names": ["Bangles", "Bracelets"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1663243818736-2b7148eeb2f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
            {"url": "https://images.unsplash.com/photo-1758995116383-f51775896add?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": False},
        ],
        "availability": "in_stock",
        "discount_percentage": 0,
    },
    {
        "name": "18K Gold Diamond Tennis Bracelet",
        "description": "A breathtaking 18K gold tennis bracelet with row of brilliant-cut diamonds. Perfect for formal occasions and gifting.",
        "seo_title": "18K Diamond Tennis Bracelet",
        "metal_name": "Gold",
        "purity_label": "18K",
        "gross_weight": 9.2,
        "net_weight": 8.7,
        "making_charge_type": "percentage",
        "making_charge_value": 18,
        "category_names": ["Bracelets"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1679156271456-d6068c543ee7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
        ],
        "availability": "in_stock",
        "discount_percentage": 15,
    },
    {
        "name": "Sterling Silver Nose Pin",
        "description": "An elegant 925 sterling silver nose pin with a tiny cubic zirconia stone. Minimalist design for everyday wear.",
        "seo_title": "Silver Nose Pin with Zirconia",
        "metal_name": "Silver",
        "purity_label": "925",
        "gross_weight": 0.5,
        "net_weight": 0.4,
        "making_charge_type": "fixed",
        "making_charge_value": 200,
        "category_names": ["Nose Pins"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1617038220319-276d3cfab638?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
        ],
        "availability": "in_stock",
        "discount_percentage": 0,
    },
    {
        "name": "22K Gold Earring Tops",
        "description": "Classic 22K gold earring tops with a simple yet elegant design. Perfect for daily wear or festive occasions.",
        "seo_title": "22K Gold Earring Tops",
        "metal_name": "Gold",
        "purity_label": "22K",
        "gross_weight": 2.8,
        "net_weight": 2.5,
        "making_charge_type": "percentage",
        "making_charge_value": 12,
        "category_names": ["Earrings"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1585960622850-ed33c41d6418?fm=jpg&q=80&w=800", "is_primary": True},
        ],
        "availability": "in_stock",
        "discount_percentage": 0,
    },
    {
        "name": "18K Diamond Eternity Ring",
        "description": "A stunning 18K gold eternity ring with channel-set diamonds all around. Symbol of everlasting love.",
        "seo_title": "18K Diamond Eternity Ring",
        "metal_name": "Gold",
        "purity_label": "18K",
        "gross_weight": 5.1,
        "net_weight": 4.7,
        "making_charge_type": "percentage",
        "making_charge_value": 16,
        "category_names": ["Rings"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1585506172580-9564a524231f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
        ],
        "availability": "made_to_order",
        "discount_percentage": 0,
    },
    {
        "name": "22K Gold Chain Necklace",
        "description": "A classic 22K gold chain necklace with traditional link pattern. 18 inches long with lobster clasp closure.",
        "seo_title": "22K Gold Chain Necklace",
        "metal_name": "Gold",
        "purity_label": "22K",
        "gross_weight": 15.0,
        "net_weight": 14.2,
        "making_charge_type": "percentage",
        "making_charge_value": 8,
        "category_names": ["Necklaces"],
        "media": [
            {"url": "https://images.unsplash.com/photo-1599475704929-b544d0afe078?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=800", "is_primary": True},
        ],
        "availability": "in_stock",
        "discount_percentage": 0,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample Aparra data matching the original website'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Product.objects.all().delete()
            Category.objects.all().delete()
            Purity.objects.all().delete()
            Metal.objects.all().delete()
            TaxClass.objects.all().delete()

        self.stdout.write('Seeding KeyValueStore (homepage, footer, settings)...')
        self._seed_kv()

        self.stdout.write('Seeding categories...')
        categories = self._seed_categories()

        self.stdout.write('Seeding metals & purities...')
        metals, purities = self._seed_metals_purities()

        self.stdout.write('Seeding tax classes...')
        tax_class = self._seed_tax()

        self.stdout.write('Seeding products...')
        self._seed_products(categories, metals, purities, tax_class)

        self.stdout.write(self.style.SUCCESS('✓ Data seeded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'  Categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  Products: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  Metals: {Metal.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  Purities: {Purity.objects.count()}'))

    def _seed_kv(self):
        kv_data = [
            ('homepage_content', HOMEPAGE_CONTENT),
            ('footer_content', FOOTER_CONTENT),
            ('shop_page_content', SHOP_CONTENT),
            ('site_settings', SITE_SETTINGS),
            ('theme_settings', {'activeHomepageTheme': 'default', 'activeProductTheme': 'default'}),
        ]
        for key, value in kv_data:
            obj, created = KeyValueStore.objects.update_or_create(
                key=key, defaults={'value': value}
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action}: {key}')

    def _seed_categories(self):
        categories = {}
        for data in SAMPLE_CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=data['name'],
                defaults={
                    'image_url': data['image_url'],
                    'is_active': True,
                }
            )
            categories[data['name']] = cat
            if created:
                self.stdout.write(f'  Created: {data["name"]}')
        return categories

    def _seed_metals_purities(self):
        metals = {}
        for data in SAMPLE_METALS:
            metal, created = Metal.objects.get_or_create(
                name=data['name'],
                defaults={
                    'price_per_gram': data['price_per_gram'],
                    'is_active': True,
                }
            )
            metals[data['name']] = metal
            if created:
                self.stdout.write(f'  Created metal: {data["name"]}')

        purities = {}
        for data in SAMPLE_PURITIES:
            metal = metals.get(data['metal_name'])
            if not metal:
                continue
            purity, created = Purity.objects.get_or_create(
                label=data['label'],
                metal=metal,
                defaults={'fineness': data['fineness'], 'is_active': True}
            )
            purities[data['label']] = purity
            if created:
                self.stdout.write(f'  Created purity: {data["label"]} ({data["metal_name"]})')

        return metals, purities

    def _seed_tax(self):
        tax, created = TaxClass.objects.get_or_create(
            name='GST 3%',
            defaults={'rate_type': 'percentage', 'rate_value': 3.0}
        )
        if created:
            self.stdout.write('  Created tax: GST 3%')
        return tax

    def _seed_products(self, categories, metals, purities, tax_class):
        for data in SAMPLE_PRODUCTS:
            if Product.objects.filter(name=data['name']).exists():
                self.stdout.write(f'  Skipped (exists): {data["name"]}')
                continue

            metal = metals.get(data['metal_name'])
            purity = purities.get(data['purity_label'])

            if not metal or not purity:
                self.stdout.write(f'  Skipped (no metal/purity): {data["name"]}')
                continue

            product = Product.objects.create(
                name=data['name'],
                description=data['description'],
                seo_title=data['seo_title'],
                metal=metal,
                purity=purity,
                tax_class=tax_class,
                gross_weight=data['gross_weight'],
                net_weight=data['net_weight'],
                making_charge_type=data['making_charge_type'],
                making_charge_value=data['making_charge_value'],
                availability=data['availability'],
                discount_percentage=data.get('discount_percentage', 0),
                is_active=True,
                auto_price_enabled=True,
                media=data['media'],
            )
            product.display_price = product.calculate_price()
            product.save()

            for cat_name in data.get('category_names', []):
                cat = categories.get(cat_name)
                if cat:
                    product.categories.add(cat)

            self.stdout.write(f'  Created: {data["name"]} → ₹{product.display_price or 0:,.0f}')
