from django.urls import path
from . import views
from .views import post_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('check_email/', views.check_email, name='check_email'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),

]
