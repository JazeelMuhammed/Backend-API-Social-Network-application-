from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import PostSerializer, LikeSerializer
from .models import Post, Like
from accounts.models import Follow
from connections.views import all_user_related_connection_instances


# Create your views here.


class PostListView(generics.ListAPIView):
    """returns all the posts"""
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')


class UserPostListView(generics.ListAPIView):
    """returns list of specific users post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        posts = self.queryset.filter(user__id=self.kwargs.get('user_id'))
        return posts.order_by('-created')


class OwnPostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = self.queryset.filter(user=self.request.user)
        return posts.order_by('-created')


class UserLikedPostsView(generics.ListAPIView):
    """returns list of all posts user liked"""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        """get a list of all posts logged in user liked"""
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class UserFollowingPostListView(generics.ListAPIView):
    """get list of all posts of followed users"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """returns all follow objects from Follow model where follower is logged in user"""
        follow_objects = Follow.objects.filter(follower=self.request.user)
        # returns a list of users who is followed by logged in user
        following_users_list = [obj.following for obj in follow_objects]
        # multi-filtering Post models based on many following users
        posts = Post.objects.filter(user__in=following_users_list)
        return posts.order_by('-created')


class ConnectedUsersPostListView(generics.ListAPIView):
    """ get all posts of users the logged in user is connected with"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """connected_user_ids returns all the users who are connected with logged in user"""
        connected_user_list = all_user_related_connection_instances(self.request.user)
        # multi-filtering Post models based on many connected users
        posts = Post.objects.filter(user__in=connected_user_list)
        return posts.order_by('-created')



