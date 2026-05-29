# Aparra Jewellery — Django

A full-featured jewellery e-commerce platform built with Django, replicating the Aparra jewellery store.

## Features

### Storefront
- Homepage with minimalist & default themes (hero slider, product carousels, category grid, testimonials, blog, Instagram section, and more)
- Shop with filtering and search
- Product detail page with image gallery, price breakup, variants, reviews
- Cart & checkout with Razorpay payment integration
- Wishlist, blog/journal, contact page
- Customer accounts — order history, address book

### Admin Dashboard (`/admin/`)
- **Products** — create/edit/delete, bulk CSV upload, media manager
- **Categories** — hierarchical categories
- **Pricing** — metal prices per gram, purities, diamond series
- **Orders** — status management, order details
- **Customers** — customer list and order history
- **Discounts** — coupon codes
- **Blog** — posts management
- **Reviews** — approve/reject customer reviews
- **Media** — image upload and library
- **Menus** — navigation menu editor
- **Reports** — sales charts, revenue analytics
- **Appearance** — theme switcher, homepage section editor (minimalist visual editor)
- **Shipping** — rates, free shipping threshold, COD
- **Payment** — Razorpay key management
- **Email** — SMTP configuration

## Tech Stack

- **Backend:** Django 5, Python 3.14
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** Tailwind CSS (CDN), Vanilla JS
- **Payments:** Razorpay
- **Static files:** WhiteNoise

## Setup

```bash
# Clone the repo
git clone https://github.com/praveshgrewal/aparra_django.git
cd aparra_django

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
RAZORPAY_KEY_ID=rzp_live_xxx
RAZORPAY_KEY_SECRET=your-secret
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@aparra.com
```

## Project Structure

```
aparra_new_django/
├── accounts/        # User auth, profiles, order history
├── blog/            # Blog/journal posts
├── dashboard/       # Admin panel views, URLs, templates
├── store/           # Products, cart, orders, homepage
├── templates/       # All HTML templates
│   ├── dashboard/   # Admin templates
│   ├── store/       # Storefront templates
│   └── partials/    # Shared navbar, footer
└── static/          # CSS and static assets
```

## Admin Login

After running the server, visit `http://127.0.0.1:8000/admin/` to access the dashboard.
