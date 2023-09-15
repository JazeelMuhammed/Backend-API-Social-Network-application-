from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render
from accounts.models import Connection, ConnectionStatus
from accounts.serializers import UserProfileListSerializer, UserSerializer, ConnectionSerializer, GetUserProfileSerializer
from accounts.models import UserProfile
from utils.permissions import IsOwnerOrReadOnly

from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

User = get_user_model()

# Create your views here.


def all_user_related_connection_instances(user):
    """ get all connection objects where logged in
    user is either sender or receiver """
    connections = Connection.objects.filter((Q(sender=user) | Q(receiver=user)) & Q(status=ConnectionStatus.accepted))
    print(connections)
    # We are using set because no duplicate connection must found
    connected_users_set = set()
    for connection in connections:
        # If a connection doesn't send a connection request to logged in user
        if connection.sender.id != user.id:
            connected_users_set.add(connection.sender.id)

        # if a connection doesn't receive a connection request from logged in user
        if connection.receiver.id != user.id:
            connected_users_set.add(connection.receiver.id)
    # stores id of the connected users either as sender or receiver
    return connected_users_set


# View to get list of all connections of logged in user
class GetUsersConnectionsView(generics.ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """returns set of logged in users_id who are either sender or receiver"""
        connection_ids = all_user_related_connection_instances(self.request.user)
        print('connection_ids', connection_ids)
        """Instead of doing Connection.objects.filter(Q(sender=first_user) | Q(receiver=first_user))
        and Connection.objects.filter(Q(sender=second_user) | Q(receiver=second_user)) and so on, we use a set{}"""
        connections = Connection.objects.filter((Q(sender__in=connection_ids) | Q(receiver__in=connection_ids)) & Q(status=ConnectionStatus.accepted))
        return connections


class RemoveFromConnectionsUserView(generics.DestroyAPIView):
    # delete connection obj from specific user
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        target_user = self.kwargs.get('user_id')
        user = request.user
        """deleting an user from connections, means we are deleting a connection instance from
        Connection model where target user is either sender or receiver"""
        connection = Connection.objects.filter((Q(sender=target_user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=target_user)))
        # if connection obj is not present, means if not a connection
        if not connection:
            raise NotFound('Not a connection yet')
        # if connection obj is present
        connection.delete()
        return Response(status=204)


class AllReceivedConnectionRequestsView(generics.ListAPIView):
    """get a list of all the pending requests send by others"""
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Connection.objects.filter(receiver=self.request.user, status=ConnectionStatus.pending)


class AllSendConnectionRequestsView(generics.ListAPIView):
    """get a list of all the pending requests send by the logged in user"""
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Connection.objects.filter(sender=self.request.user, status=ConnectionStatus.pending)


class SendConnectionRequestView(generics.CreateAPIView):
    """To send a connection request to a specific user"""
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # checks if a user already sent or received a connection request
        already_sent_or_received = Connection.objects.filter(
            (Q(sender=self.request.user) & Q(receiver=self.kwargs.get('user_id'))) |
            (Q(sender=self.kwargs.get('user_id')) & Q(receiver=self.request.user))
        ).exists()

        if already_sent_or_received:
            raise PermissionDenied('already exists a connection request')

        """Now we should save the submitted request with both sender and receiver.
        Since we doesn't specify from which model we get receiver user, we do that below"""
        receiving_user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        serializer.save(sender=self.request.user, receiver=receiving_user)


class AcceptConnectionRequestView(generics.UpdateAPIView):
    """To accept connection request sent by others, which means we are
    updating the status attribute of Connection model"""
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        # We are injecting the desired status to the request data
        is_requests_exists = Connection.objects.filter(id=self.kwargs.get('pk'), receiver=self.request.user).exists()
        print(is_requests_exists)
        if not is_requests_exists:
            raise PermissionDenied('Permission denied')
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['status'] = ConnectionStatus.accepted
        return super().update(request, *args, **kwargs)


class RejectConnectionRequestView(generics.UpdateAPIView):
    """To reject connection request send by others means we are
    updating the status attribute of Connection model to rejected"""
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        is_requests_exists = Connection.objects.filter(id=self.kwargs.get('pk'), receiver=self.request.user).exists()
        print(is_requests_exists)
        if not is_requests_exists:
            raise PermissionDenied('Permission denied')
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['status'] = ConnectionStatus.rejected
        return super().update(request, *args, **kwargs)





