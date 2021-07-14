# import json, boto3

# from logging import log
# from django.db.models.aggregates import Count, Avg
# from django.views import View
# from django.http import JsonResponse
# from datetime import datetime

# from drip_settings import ACCESS_KEY, SECRET_ACCESS_KEY
# from users.utils import login_decorator
# from .models import Like, Review, Comment
# from products.models import Product

# class ReviewView(View):
#     @login_decorator
#     def post(self, request):
#         try:
#             user    = request.user
#             content = request.POST['content']
#             rating  = request.POST['rating']
#             product = Product.objects.get(id=request.POST['product'])
            
#             s3_client = boto3.client(
#                 's3',
#                 aws_access_key_id     = ACCESS_KEY,
#                 aws_secret_access_key = SECRET_ACCESS_KEY
#             )
            
#             image      = request.FILES['filename']
#             image_time = (str(datetime.now())).replace(" ","")
#             image_type = (image.content_type).split("/")[1]                                     
            
#             s3_client.upload_fileobj(
#                 image,
#                 "dripawsbucket21",
#                 image_time+"."+image_type,
#                 ExtraArgs = {
#                     "ContentType" : image.content_type
#                 }
#             )

#             image_url = "https://dripawsbucket21.s3.ap-northeast-2.amazonaws.com/"+image_time+"."+image_type

#             Review.objects.create(
#                 user      = user,
#                 content   = content,
#                 rating    = rating,
#                 image_url = image_url if image else None,
#                 product   = product,
#             )

#             return JsonResponse({'result' : 'SUCCESS'}, status = 201)

#         except KeyError:
#             return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

#     @login_decorator
#     def get(self, request, product_id):
#         try:
#             user    = request.user
#             order   = request.GET.get('order')

#             order_conditions = {
#                 'new' : '-created_at',
#                 'old' : 'created_at',
#                 'like' : '-like_count',
#                 'unlike' : 'like_count',
#             }

#             reviews  = Review.objects.filter(product_id=product_id).annotate(like_count = Count('like')).order_by(order_conditions.get(order, '-created_at'))
            
#             review_list = [{
#                 'created_at'   : review.created_at,
#                 'user'         : review.user.name,
#                 'content'      : review.content,
#                 'rating'       : review.rating,
#                 'product'      : product_id,
#                 'like_count'   : review.like_set.count(),
#                 'review_count' : reviews.count(),
#                 'image_url'    : review.image_url,
#                 'like'         : Like.objects.filter(user_id = user.id, review_id = review.id).exists(),
#                 'user_image'   : review.user.profile_image,
#                 'avgrating' : reviews.aggregate(avgrating=Avg('rating'))
#                 } for review in reviews]
#             return JsonResponse({'result' : review_list, 'avgrating' : reviews.aggregate(avgrating=Avg('rating'))['avgrating']}, status = 200)

#         except Product.DoesNotExist:
#             return JsonResponse({"message" : 'DOES_NOT_EXIT_PRODUCT_ID'}, status = 401)

# class CommentView(View):
#     @login_decorator
#     def post(self, request):
#         try:
#             data    = json.loads(request.body)
#             content = data['content']
#             user    = request.user
#             review  = Review.objects.get(id=data['review'])
        
#             Comment.objects.create(
#                 user    = user,
#                 content = content,
#                 review  = review
#             )
#             return JsonResponse({'message' : 'SUCCESS'}, status = 201)
#         except KeyError:
#             return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

#     @login_decorator
#     def get(self, review_id):
#         try:
#             comment_list = [{
#                 'user'    : comment_list.user.id,
#                 'content' : comment_list.content,
#                 'review'  : review_id
#             }for comment_list in Comment.objects.filter(review_id = review_id)]
            
#             return JsonResponse({'result' : comment_list}, status = 200)
#         except Review.DoesNotExist:
#             return JsonResponse({"message" : 'DOES_NOT_EXIT_REVIEW_ID'}, status = 401)

# class LikeView(View):
#     @login_decorator
#     def post(self, request):
#         try:
#             data   = json.loads(request.body)
#             user   = request.user
#             review_id = data['review_id']

#             if not Review.objects.filter(id = review_id).exists():
#                 return JsonResponse({'message' : 'INVALID_REVIEW'}, status = 401)

#             if not Like.objects.filter(user = user, review_id = review_id).exists():
#                 Like.objects.create(user = user, review_id = review_id)
            
#                 return JsonResponse({'message' : 'SUCCESS'}, status= 201)

#         except KeyError:
#             return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

#     @login_decorator
#     def delete(self, request, review_id):
#         Like.objects.filter(user = request.user, review_id = review_id).delete()

#         return JsonResponse({'message' : 'SUCCESS'},status = 204)
from rest_framework import serializers
from rest_framework.serializers import Serializer
from django.http.response import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from .models import Review
from .serializer import ReviewSerializer

class ReviewsAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializers = ReviewSerializer(reviews, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = ReviewSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)