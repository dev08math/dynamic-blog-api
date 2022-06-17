from math import perm
from django.contrib import admin
from django.urls import path
from django.conf import settings
from drf_yasg import openapi     # for documentation of the API
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view  = get_schema_view(
    openapi.Info(
        title="Dyaminc-API",
        default_version="v1",
        description=" ", # idk, have to figure out
        contact= openapi.Contact(email="dummy@email.com"),
        license=openapi.License(name="XYZ License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)
urlpatterns = [
    path("readthedocs/", schema_view.with_ui("readthedocs", cache_timeout=0)),
    path(settings.base.ADMIN_URL, admin.site.urls),
]

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Dyanmic API Portal welcomes you."