from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer
from .models import Post
from accounts.models import Follow
from connections.views import all_user_related_connection_instances


# Create your views here.


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        posts = self.queryset.filter(user__id=self.kwargs.get('user_id'))
        return posts.order_by('-created')


# class UserFollowingPostListView(generics.ListAPIView):
#     """get list of all posts of followed users"""
#
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get_queryset(self):
#         """returns all follow objects from Follow model where follower is logged in user"""
#         following = Follow.objects.filter(follower=self.request.user)
#         # list of ids of users who is followed by logged in user
#         following_user_ids = [obj.following for obj in following]
#         # multi-filtering Post models based on many following users
#         posts = Post.objects.filter(user__in=following_user_ids)
#         return posts.order_by('-created')


class ConnectedUsersPostListView(generics.ListAPIView):
    """ get all posts of users the logged in user is connected with"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        connected_user_ids = all_user_related_connection_instances(self.request.user)
        # multi-filtering Post models based on many connected users
        posts = Post.objects.filter(user__in=connected_user_ids)
        return posts.order_by('-created')

