from collections import OrderedDict
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
import requests

from blog.serializers import BlogPageSerializer
from blog.serializers import AuthorSerializer


from home.models import HomePage
from rest_framework import viewsets, pagination
from .models import Author, BlogPage, BlogTagIndexPage, CommentForm, BlogIndexPage

# from .models import CommentForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
# Create your views here.

def home_viewq(request):
    # Lấy trang chủ, có thể thay đổi logic lấy trang chủ tùy theo cấu trúc của bạn
    
    home_page = HomePage.objects.first()

    # Lấy các trang blog đã xuất bản và sắp xếp theo ngày đăng
    blogpages = BlogPage.objects.live().order_by('-first_published_at')
    
    # Phân trang các trang blog
    paginator = Paginator(blogpages, 10)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'home/home_page.html',
        {
            'home_page': home_page,
            'posts': posts,
        }
    )


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
    

# def comment_view(request, pk):
#     commentform = CommentForm()
#     if request.method=='POST':
#         commentform = CommentForm(request.POST)
#         if commentform.is_valid():
#             cd = commentform.cleaned_data
#             print(cd)
#     return render(request, 'blog/blog_page.html', {'commentform':commentform})



def post(request, pk):
    # page = BlogPage.objects.get(id=page_id)

    # if request.method == 'POST':
    #     comment_form = CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         comment = comment_form.save(commit=False)
    #         comment.post = page
    #         comment.save()
    #         return redirect('blog_page', page_id=page_id)  
    # return redirect('blog_page', page_id=page_id)
    post = get_object_or_404(BlogPage, pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, user_author=request.user, post=post)
        if form.is_valid():
            form.save()
            page_current = BlogPage.objects.get(pk=pk)
            url = page_current.get_url()
            print(url)
            return HttpResponseRedirect(url)
    return render(request, 'blog/blog_page.html')

def blog_index(request):
    blogpages = BlogPage.objects.live().order_by('-date')

    paginator = Paginator(blogpages, 2)  # Hiển thị 2 bài viết blog trên mỗi trang
    page = request.GET.get('page')

    try:
        blogpages = paginator.page(page)
    except PageNotAnInteger:
        blogpages = paginator.page(1)
    except EmptyPage:
        blogpages = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog_index_page.html', {'blogpages': blogpages})


def tag_index(request):
    tag = request.GET.get('tag')  # Lấy thẻ từ tham số truy vấn
    print(tag)
    if tag:
        # Tìm trang hiển thị bài viết dựa trên tag
        try:
            tag_page = BlogTagIndexPage.objects.get(title=tag)
            # Lấy các bài viết có tag cụ thể
            blogpages = BlogPage.objects.filter(tags__name=tag)
            context = {
                'tag_page': tag_page,
                'blogpages': blogpages,
            }
        except BlogTagIndexPage.DoesNotExist:
            # Xử lý trường hợp trang tag không tồn tại
            context = {
                'tag_page': None,
                'blogpages': [],
            }
    else:
        context = {
            'tag_page': None,
            'blogpages': [],
        }

    return render(request, 'blog/tag_index_template.html', context)