from django.urls import path
from . import views


urlpatterns = [ 
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('profile/', views.UserProfile.as_view(), name='user-profile'),
    path('user-info-update/', views.updateUserInfo, name='user-profile-update'),
    path('registration/', views.UserRegistration.as_view(), name='user-registration'),
    path('logout/', views.UserLogout, name='user-logout'),
    path('change-password/', views.UserPasswordChange.as_view(), name='user-password-change'),
]