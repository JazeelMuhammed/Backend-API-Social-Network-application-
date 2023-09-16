from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from feed.models import Post
from accounts.models import Follow, Connection, ConnectionStatus
from accounts.models import UserProfile


class IsOwnerOrReadOnly(permissions.BasePermission):
    # We are implementing object level permission
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # It returns True only if obj.user matches logged in user
        return obj.user == request.user


class IsFollowingOrOwnPost(permissions.BasePermission):
    """User has the permit to like or comment his followings posts or his own post"""
    def has_object_permission(self, request, view, obj):
        post = get_object_or_404(Post, id=view.kwargs.get('pk'))
        target_user = post.user
        if request.user == target_user:
            # if the owner of the post is logged in user, then grants permission
            return True
        # otherwise only allowed to like or comment to followers posts only
        is_following = get_object_or_404(Follow, follower=request.user, following=target_user)
        if is_following:
            return True
        else:
            return False


# class IsConnectedUser(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         target_user_id = view.kwargs.get('user_id')
#         if request.user == target_user_id:
#             return True
#         target_user = get_object_or_404(UserProfile, id=target_user_id)
#
#         if target_user.private == True:
#             connection = get_object_or_404(Connection, (
#                         ((Q(sender=request.user) | Q(receiver=target_user)) & Q(status=ConnectionStatus.accepted)) |
#                         ((Q(sender=target_user) | Q(receiver=request.user)) & Q(status=ConnectionStatus.accepted))))
#             if connection:
#                 return True
#             else:
#                 return False
#         return True





