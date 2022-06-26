from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

# have to import production email

from .exceptions import NotYourProfile, CantFollowSelf
from .models import Profiles
from .serializers import ProfileSerializer, UpdateProfileSerializer, FollowingSerializer
from .pagination import ProfilePagination

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profiles.objects.all()
    pagination_class = ProfilePagination


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profiles.objects.select_related("user")
    serializer_class = ProfileSerializer()

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profiles.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profiles.objects.select_related("user")
    serializer_class = UpdateProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, username, format=None):
        try:
            prof = self.queryset.get(user__username=username)
        except Profiles.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        ### testing ####
        # vals = prof.id
        # print(prof)
        # print(vals)
        # user_name = request.user.username
        # print("Printing param...")
        # print(request.user.username)
        # print("printed")

        # data = request.data
        # print(data)
        # print("done.")
        # serializer = UpdateProfileSerializer(
        #     instance=prof, data=data, partial=True
        # )
        #####

        user_name = request.user.username
        print(username)
        print(request.user.username)
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_details(request):
    profile_instance = Profiles.objects.get(user__pkid=request.user.pkid)
    user_following_list = profile_instance.following_list()
    user_followers_list = profile_instance.followers_list()
    s_following = ProfileSerializer(user_following_list, many=True, context={'request': request})
    s_followers = ProfileSerializer(user_followers_list, many=True, context={'request': request})
    formatted_response = {
        "status_code": status.HTTP_200_OK,
        "Follows": s_following.data,
        "Number of I following": len(s_following.data),
        "Followers" : s_followers.data,
        "Number of followers I have" : len(s_followers.data)
    }
    return Response(formatted_response, status=status.HTTP_200_OK)



class FollowUnfollowAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    def get(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")
        print(specific_user)
        userprofile_instance = Profiles.objects.get(user__pkid=specific_user.pkid)
        user_following_list = userprofile_instance.following_list()
        user_followers_list = userprofile_instance.followers_list()
        s_following = ProfileSerializer(user_following_list, many=True, context={'request': request})
        s_followers = ProfileSerializer(user_followers_list, many=True, context={'request': request})
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "Follows": s_following.data,
            "Number of following": len(s_following.data),
            "Followers" : s_followers.data,
            "Number of followers" : len(s_followers.data)
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

    def post(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        if specific_user.pkid == request.user.pkid:
            raise CantFollowSelf

        userprofile_instance = Profiles.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You already follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.follow(userprofile_instance)

        subject = "A new user follows you"
        message = f"Hi there {specific_user.username}!!, the user {current_user_profile.user.username} now follows you"
        # from_email = DEFAULT_FROM_EMAIL
        # recipient_list = [specific_user.email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "detail": f"You now follow {specific_user.username}",
            }
        )

    def delete(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profiles.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if not current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You do not follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.unfollow(userprofile_instance)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "detail": f"You have unfollowed {specific_user.username}",
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
