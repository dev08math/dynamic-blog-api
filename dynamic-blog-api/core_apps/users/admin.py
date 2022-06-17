import django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from platformdirs import user_cache_dir
from .forms import UserChangeForm, UserCreationForm
from .models import User
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ["email"] # always unique
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "pkid",
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        #extra_info
        "is_staff",
        "is_active",
    ]
    list_display_links = ["id", "email"]
    list_filter = ["email", "username"]
    fieldsets = (
        (
            _("Login Creds"),
            {
                "fields":(
                    "email",
                    "password",
                )
            },
            _("Personal Info"),
            {
                "fields":(
                    "username",
                    "first_name",
                    "last_name",
                )
            },
            _("Permissions and Groups"),
            {
                "fields":(
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    #have to figure these out
                    "user_permissions",
                    "groups",
                )
            },
            _("Important Dates"),
            {
                "fields":(
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes":("wide",),
                "fields":("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email", "username", "first_name", "last_name"]

admin.site.register(User, UserAdmin)
