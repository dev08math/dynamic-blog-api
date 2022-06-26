from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static
schema_view = get_schema_view(
    openapi.Info(
        title="Dyaminc-API",
        default_version="v1",
        description=" ",
        contact=openapi.Contact(email="dummy@email.com"),
        license=openapi.License(name="XYZ License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path("apidocs/",
         schema_view.with_ui("swagger", cache_timeout=0),
         name="API Documentation"),
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Dyanmic API Portal welcomes you."