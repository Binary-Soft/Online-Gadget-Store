from django.urls import path
from . import views


urlpatterns = [ 
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('registration/', views.UserRegistration.as_view(), name='user-registration'),
    path('logout/', views.UserLogout, name='user-logout'),
]