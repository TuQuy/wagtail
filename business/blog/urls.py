
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPageViewSet


router = DefaultRouter()
router.register(r"blogpages", BlogPageViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('api/blogpage/', include(router.urls)),
]
