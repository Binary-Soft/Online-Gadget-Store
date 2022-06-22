from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:slug>/', views.SpecificCategoryAllProducts.as_view(), name='category-name'),
]