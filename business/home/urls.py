from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog import views
from .views import HomePageViewSet


router = DefaultRouter()
router.register(r"homepages", HomePageViewSet)
urlpatterns = [
    path('api/homepage/', include(router.urls)),
    path('', views.home_viewq),
    path('home/', views.home_viewq, name='home'),
    path('home/read/', views.read_view, name='read_page'),
    path('home/watch/', views.watch_view, name='watch_page'),
    path('home/learn-sport/', views.learn_sport_view, name='learn_sport_page'),
    path('home/learn-sport/blog-index', views.blog_index_page_view, name='blog_index_page'),
    path('home/event/', views.event_view, name='event_page'),
    # path('home/highlight/', views.highlight_page, name= 'highlight-page'),
]
