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
    path('', views.CreatePostView.as_view(), name='create-new-post'),
    path('<int:pk>/', views.GetUpdateDeletePostView.as_view(), name='post-detail-view'),

    # Like or unlike posts
    path('like/<int:pk>/', views.LikeOrUnlikePostView.as_view(), name='like-unlike-posts'),

    # comment or Uncomment posts
    path('comment/<int:pk>/', views.CreateCommentView.as_view(), name='comment-post'),
    path('comment/delete/<int:pk>/', views.DeleteCommentView.as_view(), name='delete-comment')
]
