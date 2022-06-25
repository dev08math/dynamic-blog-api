from rest_framework import serializers
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from django_countries.serializer_fields import CountryField

from djoser.serializers import UserCreateSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='profile.gender')
    phonenumber = PhoneNumberField(source='profile.phonenumber')
    country = CountryField(source='profile.country')
    city = serializers.CharField(source='profile.city')
    fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'fullname',
            'gender',
            'country',
            'phonenumber',
            'city',
        ]

    def get_fullname(self, obj):
        return obj.full_name

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(
            instance)  # catching the representation of the output of serializer
        if instance.is_superuser:
            representation["admin"] = True  # editing the represenation
        return representation


class CreateUserSerializer(UserCreateSerializer):    # overriding
    class Meta:
        model = User
        fields = [ 'id', 'username', 'email', 'password', 'first_name', 'last_name']
