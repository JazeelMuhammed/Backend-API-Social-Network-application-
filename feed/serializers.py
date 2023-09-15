from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    view_profile = serializers.HyperlinkedIdentityField(
        view_name='single-profile-view',
        lookup_field='user_id'
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'image', 'view_profile']
        read_only_fields = ['id', 'user', 'created']

    def get_user(self, obj):
        return f'{obj.user.username} {obj.user.id}'





