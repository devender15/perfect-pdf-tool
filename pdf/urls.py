from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('merger/', include('merger.urls')),
    path('split/', include('splitter.urls')),
    path('compress/', include('compressor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)