
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import BlogPageListAPIView
from .views import AuthorViewSet, BlogPageViewSet

router = DefaultRouter()
# router.register(r'authors', AuthorViewSet)
# router.register('', views.BlogPageListAPIView)
router.register(r'authors', AuthorViewSet)
router.register(r'blogpages', BlogPageViewSet)
urlpatterns = [
    path('', include(router.urls)),
    # path('api/blogpage/<str:id>/', views.BlogPageListAPIView.as_view()),
    # path('api/blogpage/', views.BlogPageViewSet.as_view()),
    path('api/blogpage-create/', views.BlogPageCreate.as_view(), name='create-blog'),
    path('api/', include(router.urls)),
    # path('<int:pk>/comment', views.comment_view, name='commentview')
    
]
