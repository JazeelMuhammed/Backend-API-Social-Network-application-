
from django.urls import path
from . import views


urlpatterns = [
    path('', views.GetUsersConnectionsView.as_view(), name='logged-in-user-connections'),
    path('requests/', views.AllReceivedConnectionRequestsView.as_view(), name='all-pending-requests-received'),
    path('requests/pending', views.AllSendConnectionRequestsView.as_view(), name='all-pending-requests-sent'),
    path('requests/<int:user_id>/', views.SendConnectionRequestView.as_view(), name='send-connection-request'),
    path('requests/accept/<int:pk>/', views.AcceptConnectionRequestView.as_view(), name='accept-connection-request'),
    path('requests/reject/<int:pk>/', views.RejectConnectionRequestView.as_view(), name='reject-connection-request'),
    path('remove/<int:user_id>/', views.RemoveFromConnectionsUserView.as_view(), name='remove-from-connections'),
]