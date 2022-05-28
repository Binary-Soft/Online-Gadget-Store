from django.urls import path
from . import views


urlpatterns = [ 
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('profile/', views.UserProfile.as_view(), name='user-profile'),
    path('registration/', views.UserRegistration.as_view(), name='user-registration'),
    path('logout/', views.UserLogout, name='user-logout'),
]