
from rest_framework import viewsets

from business.home.models import HomePage
from .serializers import HomePageSerializer

class HomePageViewSet(viewsets.ModelViewSet):
    queryset = HomePage.objects.all()
    serializer_class = HomePageSerializer