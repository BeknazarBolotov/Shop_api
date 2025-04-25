from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # User auth
    path('api/v1/users/register/', views.RegistrationAPIView.as_view()),
    path('api/v1/users/confirm/', views.ConfirmUserAPIView.as_view()),
    path('api/v1/users/login/', views.LoginAPIView.as_view()),
    path('api/v1/categories/', views.CategoryListCreateAPIView.as_view()),
    path('api/v1/categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('api/v1/products/', views.ProductListCreateAPIView.as_view()),
    path('api/v1/products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('api/v1/reviews/', views.ReviewListCreateAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
    path('api/v1/products/reviews/', views.ProductWithReviewsAPIView.as_view()),
]
