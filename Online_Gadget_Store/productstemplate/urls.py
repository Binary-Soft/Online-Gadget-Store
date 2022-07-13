from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:slug>/', views.SpecificCategoryAllProducts.as_view(), name='category-name'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-cart/', views.AddToCart.as_view(), name='add-to-cart'),
    path('user-orders/', views.UserOrderView.as_view(), name='user-order-list'),
    path('add-or-delete-wishlist/<int:pk>/', views.AddOrDeleteWishList.as_view(), name='add-or-delete-wishlist-product'),
]