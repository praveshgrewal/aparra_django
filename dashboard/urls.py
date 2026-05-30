from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<str:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<str:product_id>/delete/', views.product_delete, name='product_delete'),
    path('products/<str:product_id>/toggle/', views.product_toggle, name='product_toggle'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<str:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<str:category_id>/delete/', views.category_delete, name='category_delete'),

    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<str:order_id>/status/', views.order_update_status, name='order_update_status'),

    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:user_id>/', views.customer_detail, name='customer_detail'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/new/', views.blog_create, name='blog_create'),
    path('blog/<str:post_id>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<str:post_id>/delete/', views.blog_delete, name='blog_delete'),

    # Metals & Purities (managed from Pricing page)
    path('metals/', views.metals_list, name='metals_list'),
    path('metals/save/', views.metal_save, name='metal_save'),
    path('metals/<str:metal_id>/delete/', views.metal_delete, name='metal_delete'),
    path('purities/save/', views.purity_save, name='purity_save'),

    # Tax
    path('taxes/', views.tax_list, name='tax_list'),
    path('taxes/save/', views.tax_save, name='tax_save'),

    # Discounts
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/new/', views.discount_create, name='discount_create'),
    path('discounts/<str:discount_id>/delete/', views.discount_delete, name='discount_delete'),

    # Reviews
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<str:review_id>/status/', views.review_update_status, name='review_update_status'),
    path('reviews/<str:review_id>/delete/', views.review_delete, name='review_delete'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/save/', views.settings_save, name='settings_save'),

    # Appearance
    path('appearance/', views.appearance_view, name='appearance'),
    path('appearance/save/', views.appearance_save, name='appearance_save'),
    path('appearance/homepage/', views.homepage_content_view, name='homepage_content'),
    path('appearance/homepage/save/', views.homepage_content_save, name='homepage_content_save'),

    # Media
    path('media/', views.media_view, name='media'),
    path('media/upload/', views.media_upload, name='media_upload'),
    path('media/list.json', views.media_list_json, name='media_list_json'),

    # Pricing
    path('pricing/', views.pricing_view, name='pricing'),
    path('pricing/save-metals/', views.pricing_save_metals, name='pricing_save_metals'),
    path('pricing/diamond-series/save/', views.diamond_series_save, name='diamond_series_save'),
    path('pricing/diamond-series/<str:series_id>/delete/', views.diamond_series_delete, name='diamond_series_delete'),

    # Reports
    path('report/', views.report_view, name='report'),

    # Bulk Upload
    path('products/bulk-upload/', views.product_bulk_upload, name='product_bulk_upload'),
    path('products/bulk-upload/process/', views.product_bulk_upload_process, name='product_bulk_upload_process'),

    # Shipping
    path('shipping/', views.shipping_view, name='shipping'),
    path('shipping/save/', views.shipping_save, name='shipping_save'),

    # Payment settings
    path('settings/payment/', views.payment_settings_view, name='payment_settings'),
    path('settings/payment/save/', views.payment_settings_save, name='payment_settings_save'),

    # Email settings
    path('settings/email/', views.email_settings_view, name='email_settings'),
    path('settings/email/save/', views.email_settings_save, name='email_settings_save'),

    # Menus
    path('menus/', views.menus_view, name='menus'),
    path('menus/save/', views.menus_save, name='menus_save'),

    # Minimalist homepage visual editor
    path('appearance/minimalist/', views.minimalist_editor_view, name='minimalist_editor'),
    path('appearance/minimalist/save/', views.minimalist_editor_save, name='minimalist_editor_save'),
]
