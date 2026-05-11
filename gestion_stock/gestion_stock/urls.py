from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('partenaires/', include('partenaires.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('catalogue.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('stock/', include('stock.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
