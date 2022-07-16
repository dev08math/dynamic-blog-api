from django.contrib import admin

from .models import Profiles


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "gender", "phonenumber", "country", "city"]
    list_filter = ["gender", "country", "city"]
    list_display_links = ["id", "pkid"]


admin.site.register(Profiles, ProfileAdmin)