from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import include, path

from catalogue.views import dashboard
from core.views import parametres

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="accounts:login", permanent=False), name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("parametres/", parametres, name="parametres"),
    path("accounts/", include("accounts.urls")),
    path("partenaires/", include("partenaires.urls")),
    path("catalogue/", include("catalogue.urls")),
    path("stock/", include("stock.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
