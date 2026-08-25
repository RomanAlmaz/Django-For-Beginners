from django.contrib.auth import views as auth_views
from django.urls import path

from shop import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/review/', views.review_create, name='review_create'),
    path(
        'products/<int:pk>/review/<int:review_pk>/edit/',
        views.review_update,
        name='review_update',
    ),
    path(
        'products/<int:pk>/review/<int:review_pk>/delete/',
        views.review_delete,
        name='review_delete',
    ),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/<int:pk>/add/', views.cart_add, name='cart_add'),
    path('cart/<int:pk>/update/', views.cart_update, name='cart_update'),
    path('cart/<int:pk>/remove/', views.cart_remove, name='cart_remove'),
    path('accounts/register/', views.register, name='register'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='shop/login.html'),
        name='login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
