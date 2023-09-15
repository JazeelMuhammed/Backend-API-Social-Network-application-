from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import UserProfile, Follow
from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()

# Create Your Views Here


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]


class GetUserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.GetUserProfileSerializer
    lookup_field = 'user_id'
    permission_classes = [IsOwnerOrReadOnly, ]


class CreateUserProfileView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [permissions.AllowAny, ]


class FollowUnfollowUsersView(generics.CreateAPIView, mixins.DestroyModelMixin):
    # We are posting a follow request
    # Also deleting a follow request
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_to_follow = get_object_or_404(User, id=self.kwargs.get('user_id'))
        already_following = Follow.objects.filter(follower=self.request.user, following=user_to_follow).exists()

        # if it returns True
        if already_following:
            raise PermissionDenied('already following')
        # else we create and save the Follow object in the db.
        serializer.save(follower=self.request.user, following=user_to_follow)

    def delete(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(User, id=self.kwargs.get('user_id'))
        follow = get_object_or_404(Follow, follower=self.request.user, following=user_to_unfollow)
        follow.delete()
        return Response(status=204)


class GetUserFollowersView(generics.ListAPIView):
    # get all the followers of authenticated user
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super(GetUserFollowersView, self).get_queryset()
        return qs.filter(following=self.request.user)


class GetUserFollowingView(generics.ListAPIView):
    # get all the users who are followed by logged in user
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super(GetUserFollowingView, self).get_queryset()
        return qs.filter(follower=self.request.user)


