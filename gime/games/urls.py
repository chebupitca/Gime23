from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload/', views.upload_game, name='upload_game'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
     path('user/<int:user_id>/', views.user_profile, name='user_profile'),
]