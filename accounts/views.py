from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import UserProfile, Follow, Connection, ConnectionStatus
from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()

# Create Your Views Here


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]


class GetUserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.GetUserProfileSerializer
    lookup_field = 'user_id'
    permission_classes = [IsOwnerOrReadOnly, ]

    def retrieve(self, request, *args, **kwargs):
        auth_user = self.request.user
        target_user = self.kwargs.get('user_id')
        instance = self.get_object()

        if instance.private == True:
            is_connected = Connection.objects.filter(((Q(sender=auth_user) & Q(receiver=target_user)) & Q(status=ConnectionStatus)) |
                                                   ((Q(sender=target_user) & Q(receiver=auth_user)) & Q(status=ConnectionStatus))).exists()
            if is_connected:
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied('Private profile')
        else:
            instance = self.get_object()
            serializer = serializers.GetUserProfileSerializer(instance)
            return Response(serializer.data)


class GetOrUpdatePrivateUserData(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.MyProfileSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        self.kwargs['pk'] = self.request.user.id
        return self.queryset


class CreateUserProfileView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [permissions.AllowAny, ]


class SuggestedUsersView(generics.ListAPIView):
    """get a list of suggested users"""
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following = Follow.objects.filter(follower=self.request.user)
        my_following = [obj.following for obj in following]
        suggested_follow_objects = Follow.objects.filter(follower__in=my_following)
        suggested_users = [obj.following for obj in suggested_follow_objects]
        all_suggestions = UserProfile.objects.filter(user__in=suggested_users)
        already_following = Follow.objects.filter(follower=self.request.user, following__in=suggested_users)
        already_following_users = [obj.following for obj in already_following]
        already_following_suggestions = UserProfile.objects.filter(user__in=already_following_users)
        final_suggestions = all_suggestions.difference(already_following_suggestions)[:6]
        print(final_suggestions)
        return final_suggestions


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


