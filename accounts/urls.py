from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.account_view, name='account'),
    path('orders/', views.account_orders, name='orders'),
    path('orders/<str:order_id>/', views.account_order_detail, name='order_detail'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('save-address/', views.save_address, name='save_address'),
    path('delete-address/', views.delete_address, name='delete_address'),
]
