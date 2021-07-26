from products.views import ProductAPIView, ProductsAPIView, RecommendAPIView
from django.urls import path

urlpatterns = [
    path('/<str:pk>', ProductAPIView.as_view()),
    path('', ProductsAPIView.as_view()),
    path('/recommend/<str:pk>', RecommendAPIView.as_view())
]
