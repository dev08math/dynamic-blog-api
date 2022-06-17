from sre_constants import MAX_UNTIL
from tabnanny import verbose
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    # By default, Django gives each model the following field:
    #     id = models.BigAutoField(primary_key=True, **options) [See settings]
    #     BigAutoField is a 64-bit integer, much like an AutoField except that it is guaranteed to fit numbers from 1 to 9223372036854775807
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("username"), db_index=True, max_length=255, unique=True)
    first_name = models.CharField(verbose_name=_("first_name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last_name"), max_length=50)
    email = models.EmailField(verbose_name=_("last_name"), db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = ["email"] # will have to create a custom authentication backend that tries to look up the user on the 'email' or 'username' fields.
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"