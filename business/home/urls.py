
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomePageViewSet


router = DefaultRouter()
router.register(r"homepages", HomePageViewSet)
urlpatterns = [
    path('api/homepage/', include(router.urls)),
    
]
