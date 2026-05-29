from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('admin/', include('dashboard.urls', namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
