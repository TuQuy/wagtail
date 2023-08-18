from collections import OrderedDict
from django.http import Http404, JsonResponse
from django.shortcuts import render
import requests

from blog.serializers import BlogPageSerializer
from blog.serializers import AuthorSerializer


from home.models import HomePage
from rest_framework import viewsets, pagination
from .models import Author, BlogPage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
# Create your views here.

def home_viewq(request):
    home_page = HomePage.objects.first()  # Lấy trang chủ, có thể thay đổi logic lấy trang chủ tùy theo cấu trúc của bạn
    return render(request, 'home_page.html', {'home_page': home_page})


# class BlogPageListAPIView(generics.RetrieveAPIView):
#     queryset = BlogPage.objects.all()
#     serializer_class = BlogPageSerializer

#     # def get(self, request, *args, **kwargs):
#     #     try:
#     #         instance = self.get_object()
#     #         serializer = self.serializer_class(instance, context={'request': request})
#     #         return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)
#     #     except BlogPage.DoesNotExist:
#     #         return Response(data={}, status=status.HTTP_404_NOT_FOUND)

#     def get_object(self):
#         queryset = self.get_queryset()
       
#         id = self.kwargs.get('id')
       
#         if id is not None:
#             queryset = self.queryset.filter(id=id)
#         try:
#             obj = queryset.get()
#         except BlogPage.DoesNotExist:
#             raise Http404("No matching Venue found.")
#         return obj
    
#     def get(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             serializer = self.serializer_class(instance, context={'request': request})
#             return Response(data={'data': serializer.data},
#                             status=status.HTTP_200_OK)
#         except Exception:
#             return Response(data={},
#                             status=status.HTTP_404_NOT_FOUND)

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 3  # Số items trên mỗi page
    page_size_query_param = 'page_size'
    max_page_size = 100

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BlogPageViewSet(viewsets.ModelViewSet):
    queryset = BlogPage.objects.all().prefetch_related('authors')
    serializer_class = BlogPageSerializer
    pagination_class = CustomPageNumberPagination

class BlogPageCreate(generics.CreateAPIView):
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'data':serializer.data}, status=status.HTTP_201_CREATED)
    