from django.urls import path
from reviews.views import ReviewsAPIView

urlpatterns = [
   path('', ReviewsAPIView.as_view()),
]