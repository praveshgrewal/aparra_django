from django.db import models
from django.conf import settings
import uuid


def generate_id():
    return str(uuid.uuid4())[:8]


class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    icon = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Metal(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    price_per_gram = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Purity(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name='purities')
    label = models.CharField(max_length=50)
    fineness = models.FloatField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'purities'

    def __str__(self):
        return f"{self.label} ({self.metal.name})"


class TaxClass(models.Model):
    RATE_TYPE_CHOICES = [('percentage', 'Percentage'), ('fixed', 'Fixed')]
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    name = models.CharField(max_length=100)
    rate_type = models.CharField(max_length=20, choices=RATE_TYPE_CHOICES, default='percentage')
    rate_value = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DiamondSeries(models.Model):
    DIAMOND_TYPE_CHOICES = [('Both', 'Both'), ('Natural', 'Natural'), ('Lab', 'Lab')]
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    name = models.CharField(max_length=255)
    rate_per_carat = models.FloatField()
    description = models.TextField(blank=True, null=True)
    diamond_type = models.CharField(max_length=20, choices=DIAMOND_TYPE_CHOICES, default='Both')
    is_active = models.BooleanField(default=True)
    brand_margin = models.FloatField(null=True, blank=True)
    certification_cost = models.FloatField(null=True, blank=True)
    clarity = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    cut = models.CharField(max_length=50, blank=True, null=True)
    setting_charges = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'diamond series'

    def __str__(self):
        return self.name


class Product(models.Model):
    MAKING_CHARGE_TYPE_CHOICES = [('fixed', 'Fixed'), ('percentage', 'Percentage')]
    AVAILABILITY_CHOICES = [('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock'), ('made_to_order', 'Made to Order')]
    DISCOUNT_TYPE_CHOICES = [('percentage', 'Percentage'), ('fixed', 'Fixed')]

    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    name = models.CharField(max_length=500)
    categories = models.ManyToManyField(Category, blank=True, related_name='products')
    metal = models.ForeignKey(Metal, on_delete=models.SET_NULL, null=True, blank=True)
    purity = models.ForeignKey(Purity, on_delete=models.SET_NULL, null=True, blank=True)
    tax_class = models.ForeignKey(TaxClass, on_delete=models.SET_NULL, null=True, blank=True)
    gross_weight = models.FloatField(default=0)
    net_weight = models.FloatField(default=0)
    making_charge_type = models.CharField(max_length=20, choices=MAKING_CHARGE_TYPE_CHOICES, default='percentage')
    making_charge_value = models.FloatField(default=0)
    auto_price_enabled = models.BooleanField(default=True)
    manual_price = models.FloatField(null=True, blank=True)
    seo_title = models.CharField(max_length=500, blank=True)
    seo_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    variants = models.JSONField(default=list, blank=True)
    media = models.JSONField(default=list, blank=True)
    certificates = models.JSONField(default=list, blank=True)
    price_breakup = models.JSONField(default=dict, blank=True)
    display_price = models.FloatField(null=True, blank=True)
    availability = models.CharField(max_length=30, choices=AVAILABILITY_CHOICES, default='in_stock')
    has_diamonds = models.BooleanField(default=False)
    diamond_details = models.JSONField(default=list, blank=True)
    cross_sell_products = models.JSONField(default=list, blank=True)
    upsell_products = models.JSONField(default=list, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    feature_tabs = models.JSONField(default=list, blank=True)
    gallery_images = models.JSONField(default=list, blank=True)
    has_ring_size = models.BooleanField(default=False)
    has_size_dimensions = models.BooleanField(default=False)
    show_gallery_grid = models.BooleanField(default=False)
    has_stones = models.BooleanField(default=False)
    stone_details = models.JSONField(default=list, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    more_info = models.TextField(blank=True)
    original_price = models.FloatField(null=True, blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, null=True, blank=True)
    discount_value = models.FloatField(null=True, blank=True)
    making_charge_discount = models.FloatField(null=True, blank=True, help_text="Discount % applied to making charge and resulting tax")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_primary_image(self):
        if self.media and len(self.media) > 0:
            return self.media[0].get('url', '')
        return ''

    def get_final_price(self):
        if self.auto_price_enabled:
            return self.display_price or self.calculate_price()
        return self.manual_price or 0

    def calculate_price(self):
        bp = self.get_price_breakup()
        return bp.get('total', 0)

    def get_price_breakup(self):
        if not self.metal or not self.purity or not self.tax_class:
            return {}
        price_per_gram = self.metal.price_per_gram * self.purity.fineness
        metal_value = round(price_per_gram * self.net_weight)
        if self.making_charge_type == 'fixed':
            making_charge_base = round(self.making_charge_value)
        else:
            making_charge_base = round(metal_value * (self.making_charge_value / 100))
        diamond_value = 0
        if self.has_diamonds and self.diamond_details:
            for d in self.diamond_details:
                if d.get('price') and d['price'] > 0:
                    diamond_value += d['price']
                else:
                    diamond_value += round(d.get('rate_per_carat', 0) * d.get('weight', 0))

        mc_discount = self.making_charge_discount or 0
        if mc_discount > 0:
            making_charge_disc = round(making_charge_base * (1 - mc_discount / 100))
            orig_subtotal = metal_value + making_charge_base + diamond_value
            disc_subtotal = metal_value + making_charge_disc + diamond_value
            if self.tax_class.rate_type == 'percentage':
                gst_orig = round(orig_subtotal * (self.tax_class.rate_value / 100))
                gst_disc = round(disc_subtotal * (self.tax_class.rate_value / 100))
            else:
                gst_orig = gst_disc = round(self.tax_class.rate_value)
            return {
                'metal_value': metal_value,
                'diamond_value': diamond_value,
                'making_charge': making_charge_disc,
                'making_charge_original': making_charge_base,
                'gst': gst_disc,
                'gst_original': gst_orig,
                'total': disc_subtotal + gst_disc,
                'total_original': orig_subtotal + gst_orig,
            }

        subtotal = metal_value + making_charge_base + diamond_value
        if self.tax_class.rate_type == 'percentage':
            gst = round(subtotal * (self.tax_class.rate_value / 100))
        else:
            gst = round(self.tax_class.rate_value)
        return {
            'metal_value': metal_value,
            'making_charge': making_charge_base,
            'diamond_value': diamond_value,
            'gst': gst,
            'total': subtotal + gst,
        }

    @property
    def price_before_discount(self):
        if self.original_price and self.original_price > 0:
            return self.original_price
        if self.making_charge_discount and self.auto_price_enabled:
            bp = self.computed_price_breakup
            return bp.get('total_original') if bp else None
        if self.discount_percentage:
            return self.display_price or self.manual_price
        return None

    @property
    def price_after_discount(self):
        if self.original_price and self.original_price > 0:
            return self.display_price or self.manual_price
        if self.making_charge_discount and self.auto_price_enabled:
            return self.display_price
        if self.discount_percentage:
            base = self.display_price or self.manual_price
            if base:
                return round(base * (1 - self.discount_percentage / 100))
        return self.display_price or self.manual_price

    @property
    def computed_price_breakup(self):
        if self.price_breakup:
            return self.price_breakup
        return self.get_price_breakup()


class ProductReview(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer_name} for {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('confirmed', 'Confirmed'),
        ('processing', 'Processing'), ('shipped', 'Shipped'),
        ('delivered', 'Delivered'), ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=255, blank=True)
    customer_email = models.CharField(max_length=255, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    items = models.JSONField(default=list)
    shipping_address = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount = models.JSONField(default=dict, blank=True, null=True)
    shipping_carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='pending')
    subtotal = models.FloatField(default=0)
    total = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class Discount(models.Model):
    TYPE_CHOICES = [('percentage', 'Percentage'), ('fixed_amount', 'Fixed Amount')]
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    min_purchase = models.FloatField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    usage_limit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.code


class Menu(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    name = models.CharField(max_length=100)
    items = models.JSONField(default=list)

    def __str__(self):
        return self.name


class KeyValueStore(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.JSONField(default=dict)

    def __str__(self):
        return self.key


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.email}"
