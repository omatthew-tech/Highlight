from django.urls import path
from . import views
from .views import  like_post
from .views import search

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('check_email/', views.check_email, name='check_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit-profile'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('search/', search, name='search'),
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend_requests/', views.view_friend_requests, name='view_friend_requests'),
    path('respond_friend_request/<int:request_id>/<str:action>/', views.respond_friend_request, name='respond_friend_request'),
]   
