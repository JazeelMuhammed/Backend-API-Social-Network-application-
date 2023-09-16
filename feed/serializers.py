from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Post, Like, Comment


class LikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = []


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_date']

    def get_user(self, obj):
        return f'{obj.user.username} of id {obj.user.id}'


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']


class DeleteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    view_profile = serializers.HyperlinkedIdentityField(
        view_name='single-profile-view',
        lookup_field='user_id'
    )
    likes = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'image', 'likes', 'like_count', 'comments', 'comment_count', 'view_profile']
        read_only_fields = ['id', 'user', 'created']

    def get_user(self, obj):
        return f'{obj.user.username} of id {obj.user.id}'

    def get_likes(self, obj):
        """here obj is Post"""
        likes = obj.likes.all()
        serializer = LikeListSerializer(likes, many=True)
        return serializer.data

    def get_like_count(self, obj):
        likes = obj.likes.all()
        return likes.count()

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return serializer.data

    def get_comment_count(self, obj):
        comments = obj.comments.all()
        return comments.count()
















