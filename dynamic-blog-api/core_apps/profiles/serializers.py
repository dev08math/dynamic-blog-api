from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profiles


class ProfileSerializer(serializers.ModelSerializer):
    # "user" will guide to 'AUTH_USER_MODEL' via OneToOne mapping
    username = serializers.CharField(source="user.username")
    firstname = serializers.CharField(source="user.first_name")
    lastname = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    # testing : using full_name getter method from user models
    fullname = serializers.SerializerMethodField(read_only=True)

    profile_dp = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profiles
        fields = [
            'username',
            'firstname',
            'lastname',
            'email',
            'fullname',
            'id',
            'about_me',
            'gender',
            'phonenumber',
            'country',
            'city',
            'profile_dp',
            'twitter_handle',
            'following',
        ]

    def get_profile_dp(self, obj):   # object from Profiles class
        return obj.profile_pic.url

    def get_following(self, instance):    # checking if the profile being viewed is being followed by the current user, if logged in
        request = self.context.get("request", None)
        if request is None:
            return None
        if request.user.is_anonymous:
            return False

        # using the 'related_name=profile' in Profiles to access the corresponding obj by the user obj
        current_user_profile = request.user.profile   # accessing current user's profile using request
        followee = instance    # custom queryset of having profile obj(s) in consideration passed as input when ProfileSerializer is called
        following_status = current_user_profile.check_following(followee)
        return following_status
    
    def get_fullname(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

class UpdateProfileSerializer(serializers.ModelSerializer):   # POST request
    country = CountryField(name_only=True)

    class Meta:
        model = Profiles
        fields = [
            "phonenumber",
            "profile_pic",
            "about_me",
            "gender",
            "country",
            "city",
            "twitter_handle",
        ]

class FollowingSerializer(serializers.ModelSerializer):  # have to figure this out

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    following = serializers.BooleanField(default=True)

    class Meta:
        model = Profiles
        fields = [
            "username",
            "first_name",
            "last_name",
            "profile_pic",
            "about_me",
            "twitter_handle",
            "following",
        ]
