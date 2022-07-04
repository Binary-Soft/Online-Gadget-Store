from django.urls import path
from . import views


urlpatterns = [ 
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('update-profile/', views.UpdateUserProfile.as_view(), name='update-user-profile'),
    path('user-info-update/', views.updateUserInfo, name='user-profile-update'),
    path('registration/', views.UserRegistration.as_view(), name='user-registration'),
    path('logout/', views.UserLogout, name='user-logout'),
    path('change-password/', views.UserPasswordChange.as_view(), name='user-password-change'),
    path('password-reset/', views.UserPasswordReset.as_view(), name='user-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetConfirm.as_view(), 
    name='password_reset_confirm'),
    path('password-reset-done/', views.UserPasswordResetDone.as_view(), name='password_reset_done'),
    path('password-reset-complete/', views.UserPasswordResetComplete.as_view(), name='password_reset_complete'),
]