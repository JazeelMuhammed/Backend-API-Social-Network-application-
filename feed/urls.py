"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='show-all-posts'),
    path('<int:user_id>/', views.UserPostListView.as_view(), name='specific-user-posts'),
    path('me/', views.OwnPostListView.as_view(), name='my-posts'),

    # url to get all posts of users who are followed by logged in user
    path('following/', views.UserFollowingPostListView.as_view(), name='following-users-posts'),
    # url to get all posts of users who are connected with logged in user
    path('connections/', views.ConnectedUsersPostListView.as_view(), name='connected-users-posts'),

    # user liked posts
    path('likedPosts/', views.UserLikedPostsView.as_view(), name='user-liked-posts'),
]
