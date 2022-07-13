from django.urls import path

from . import views


urlpatterns = [ 
    path('create-checkout-session/', views.CreateCheckoutSession.as_view(), name='create-checkout'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancleView.as_view(), name='cancle'),
    path('webhook/', views.my_webhook_view, name='webhook'),
]