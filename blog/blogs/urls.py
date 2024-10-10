from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home,name='home'),
    path("signup",RegisterView.as_view(),name='signup'),
    path("",LoginView.as_view(),name='login'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('profile/edit',EditProfileView.as_view(), name='edit_profile'),
    path('logout',views.signout,name='logout'),
    path('base-account',views.index,name='base-account'),
    path('create_post', CreatePostView.as_view(), name='create_post'),
    path('view_posts', ViewPostsView.as_view(), name='view_posts'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('edit/<int:post_id>/', edit_post, name='edit_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
]