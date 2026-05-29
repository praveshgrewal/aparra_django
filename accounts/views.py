import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User
from store.models import Order


def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:homepage')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        phone = request.POST.get('phone', '')

        if not name or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/register.html')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(email=email, password=password, name=name, phone_number=phone)
        login(request, user)
        messages.success(request, f'Welcome, {name}!')
        return redirect('store:homepage')
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:homepage')
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next', '/')
            return redirect(next_url)
        messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html', {'next': request.GET.get('next', '/')})


def logout_view(request):
    logout(request)
    return redirect('store:homepage')


@login_required
def account_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'accounts/account.html', {'orders': orders})


@login_required
def account_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/orders.html', {'orders': orders})


@login_required
def account_order_detail(request, order_id):
    order = Order.objects.filter(id=order_id, user=request.user).first()
    if not order:
        messages.error(request, 'Order not found.')
        return redirect('accounts:orders')
    return render(request, 'accounts/order_detail.html', {'order': order})


@login_required
@require_POST
def update_profile(request):
    user = request.user
    user.name = request.POST.get('name', user.name)
    if request.POST.get('phone'):
        user.phone_number = request.POST.get('phone')
    user.save()
    messages.success(request, 'Profile updated successfully.')
    return redirect('accounts:account')


@login_required
@require_POST
def change_password(request):
    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('new_password', '')
    confirm_password = request.POST.get('confirm_password', '')
    if not request.user.check_password(old_password):
        messages.error(request, 'Current password is incorrect.')
        return redirect('accounts:account')
    if new_password != confirm_password:
        messages.error(request, 'New passwords do not match.')
        return redirect('accounts:account')
    request.user.set_password(new_password)
    request.user.save()
    messages.success(request, 'Password changed successfully. Please log in again.')
    return redirect('accounts:login')


@login_required
@require_POST
def save_address(request):
    data = json.loads(request.body)
    addresses = request.user.addresses or []
    import uuid
    new_address = {
        'id': str(uuid.uuid4())[:8],
        'name': data.get('name', ''),
        'phone': data.get('phone', ''),
        'address_line1': data.get('address_line1', ''),
        'address_line2': data.get('address_line2', ''),
        'city': data.get('city', ''),
        'state': data.get('state', ''),
        'pincode': data.get('pincode', ''),
        'country': data.get('country', 'India'),
    }
    addresses.append(new_address)
    request.user.addresses = addresses
    request.user.save()
    return JsonResponse({'success': True, 'address': new_address})


@login_required
@require_POST
def delete_address(request):
    data = json.loads(request.body)
    address_id = data.get('id')
    addresses = [a for a in (request.user.addresses or []) if a.get('id') != address_id]
    request.user.addresses = addresses
    if request.user.default_address_id == address_id:
        request.user.default_address_id = None
    request.user.save()
    return JsonResponse({'success': True})
