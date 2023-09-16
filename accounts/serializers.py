from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import UserProfile, Follow, Connection, ConnectionStatus
from drf_writable_nested import WritableNestedModelSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class UserProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='get_username')
    connections = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'connections', 'followers', 'following', )
        read_only_fields = ('username', 'user_id',)

    def get_connections(self, obj):
        connections = Connection.objects.filter((Q(sender=obj.user) | Q(receiver=obj.user)) & Q(status=ConnectionStatus.accepted))
        return connections.count()

    def get_followers(self, obj):
        followers = obj.user.following.all()
        return followers.count()

    def get_following(self, obj):
        following = obj.user.follower.all()
        return following.count()


class PrivateUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('username', 'profile_picture', 'bio')

    def get_username(self, obj):
        return obj.user.username


class MyProfileSerializer(WritableNestedModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'bio', 'location', 'private', )
        read_only_fields = ('username', 'user_id',)

    def get_username(self, obj):
        return obj.user.username


class GetUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    connections = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'followers', 'following', 'connections', 'first_name', 'last_name', 'location', 'bio', 'profile_picture', 'private',]

    def get_username(self, obj):
        return obj.user.username

    def get_followers(self, obj):
        # gets all users who is following logged in user
        followers = obj.user.following.all()
        serializer = FollowSerializer(followers, many=True)
        return serializer.data

    def get_following(self, obj):
        # gets all users who followed by logged in user
        following = obj.user.follower.all()
        serializer = FollowSerializer(following, many=True)
        return serializer.data

    def get_connections(self, obj):
        connections = Connection.objects.filter((Q(sender=obj.user) | Q(receiver=obj.user)) & Q(status=ConnectionStatus.accepted))
        serializer = ConnectionSerializer(connections, many=True)
        return serializer.data


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], None, validated_data['password'])
        return user


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField(source='follower')
    following = serializers.SerializerMethodField(source='following')

    class Meta:
        model = Follow
        fields = ('follower', 'following', )
        read_only = True

    def get_follower(self, obj):
        return obj.follower.username

    def get_following(self, obj):
        return obj.following.username


class ConnectionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = ['id', 'sender', 'receiver', 'status']

    def get_sender(self, obj):
        return obj.sender.username

    def get_receiver(self, obj):
        return obj.receiver.username







