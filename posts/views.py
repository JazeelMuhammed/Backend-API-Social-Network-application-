from django.http import HttpResponse, JsonResponse
from feed.models import Post, Like, Comment
from feed.serializers import PostSerializer, LikeSerializer, CreateCommentSerializer, DeleteCommentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from utils.permissions import IsFollowingOrOwnPost

# rest famework
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from rest_framework import status

# Create your views here


class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # creating new post with user as requested user
        serializer.save(user=self.request.user)


class GetUpdateDeletePostView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'


class LikeOrUnlikePostView(generics.CreateAPIView, mixins.DestroyModelMixin):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsFollowingOrOwnPost]

    def perform_create(self, serializer):
        user = self.request.user
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        already_liked = Like.objects.filter(post=post, user=user).exists()
        if already_liked:
            raise PermissionDenied('already liked')
        serializer.save(user=user, post=post)

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        like_instance = get_object_or_404(Like, user=self.request.user, post=post)
        like_instance.delete()
        return Response(status=204)


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsFollowingOrOwnPost]
    lookup_field = 'pk'

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        user = self.request.user
        serializer.save(user=user, post=post)


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = DeleteCommentSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()
