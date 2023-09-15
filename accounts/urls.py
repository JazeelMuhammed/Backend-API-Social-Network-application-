
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.UserProfileListAPIView.as_view(), name='list-all-profiles'),
    path('create/', views.CreateUserProfileView.as_view(), name='create-new-user'),
    path('<int:user_id>/', views.GetUserProfileView.as_view(), name='single-profile-view'),

    # follow urls
    path('follow/<int:user_id>/', views.FollowUnfollowUsersView.as_view(), name='follow-or-unfollow-user-view'),
    path('followers/', views.GetUserFollowersView.as_view(), name='user-followers-view'),
    path('following/', views.GetUserFollowingView.as_view(), name='user-following-view'),

    # connection urls
    path('connections/', include('connections.urls')),

    path('suggested/', views.SuggestedUsersView.as_view(), name='suggested-users'),
]