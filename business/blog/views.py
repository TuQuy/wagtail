from django.shortcuts import render

from blog.serializers import BlogPageSerializer

from home.models import HomePage
from rest_framework import viewsets
from .models import BlogPage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

def home_viewq(request):
    home_page = HomePage.objects.first()  # Lấy trang chủ, có thể thay đổi logic lấy trang chủ tùy theo cấu trúc của bạn
    return render(request, 'home_page.html', {'home_page': home_page})


class BlogPageViewSet(viewsets.ModelViewSet):
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageSerializer
    
    def get(self, request, format=None):
        # Lấy tất cả các bài viết từ model BlogPage
        blog_posts = BlogPage.objects.all()

        # Tạo một danh sách để chứa dữ liệu bài viết (loại bỏ trường 'authors')
        data = []
        for post in blog_posts:
            post_data = {
                'date': post.date,
                'intro': post.intro,
                'body': post.body,
                'tags': [tag.name for tag in post.tags.all()],
                'main_image': post.main_image().url if post.main_image() else None,
            }
            data.append(post_data)

        return Response(data)
    
    def perform_create(self, serializer):
        serializer.save()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Lấy đối tượng bài viết cụ thể dựa trên ID
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
