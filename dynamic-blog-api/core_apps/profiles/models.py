from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Profiles(TimeStampedUUIDModel):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        NA = "n/a", _("n/a")

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    about_me = models.TextField(
        verbose_name=_("About me"), default=_("Say something about yourself...")
    )
    gender = models.CharField(
        verbose_name=_("Gender"), choices=Gender.choices, default=Gender.NA
    )
    phonenumber = PhoneNumberField(
        verbose_name=_("Phonenumber"), max_length=13, default="+919999999999"
    )
    country = CountryField(verbose_name=_("Country"), default="IN")
    city = models.CharField(verbose_name=_("City"), max_length=100)
    profile_pic = models.ImageField(default="", upload_to="")  # have to fix this
    twitter_handle = models.CharField(
        verbose_name=_("Twitter Handle"), max_length=20, blank=True
    )
    follows = models.ManyToManyField(
        "self", related_name="followed_by", blank=True, symmetrical=False
    )  # followers will follow the person they want but the one who they are following doesn't necessarily need to follow them back that's why symmetrical = False

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

    def following_list(self):
        return self.follows.all()

    def followers_list(self):
        return self.follow_by.all()

    def follow(self, profile):  # have to be given proper profile obj
        return self.follows.add(profile)

    def unfollow(self, profile):
        return self.follows.remove(profile)

    def check_following(self, profile):
        return self.follows.filter(id=profile.id).exists()

    def check_followed_by(self, profile):  # have some doubts whether it will work as only a single relationship table (follows - > followed_by) is being made
        return self.followed_by.filter(id=profile.id).exists()
