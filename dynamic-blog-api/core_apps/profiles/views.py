from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

# have to import production email

from .exceptions import NotYourProfile, CantFollowSelf
from .models import Profiles
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer, FollowingSerializer
from .pagination import ProfilePagination

User = get_user_model()

# @api_view(["GET"])
# @permission_classes([permissions.AllowAny])
# def get_all_profiles(request):
#     profiles = Profile.objects.all()
#     serializer = ProfileSerializer(profiles, many=True)
#     namespaced_response = {"profiles": serializer.data}
#     return Response(namespaced_response, status=status.HTTP_200_OK)

# @api_view(["GET"])
# @permission_classes([permissions.AllowAny])
# def get_profile_details(request,username):
#     try:
#         user_profile = Profile.objects.get(user__username=username)
#     except Profile.DoesNotExist:
#         raise NotFound('A profile with this username does not exist...')

#     serializer = ProfileSerializer(user_profile, many=False)
#     formatted_response = {"profile": serializer.data}
#     return Response (formatted_response, status=status.HTTP_200_OK)
