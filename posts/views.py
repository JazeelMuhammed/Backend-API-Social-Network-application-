from django.http import HttpResponse, JsonResponse
from feed.models import Post
from feed.serializers import PostSerializer

# rest famework
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

# Create your views here


class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        # creating new post with user as requested user
        serializer.save(user=self.request.user)


class GetUpdateDeletePostView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'


