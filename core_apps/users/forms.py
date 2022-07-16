from django.contrib.auth import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):

    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    class Meta(forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {
                "unique": _("This username has already been taken")
            },
        }
