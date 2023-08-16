from django.shortcuts import render

from business.home.models import HomePage

# Create your views here.

def home_viewq(request):
    home_page = HomePage.objects.first()  # Lấy trang chủ, có thể thay đổi logic lấy trang chủ tùy theo cấu trúc của bạn
    return render(request, 'home_page.html', {'home_page': home_page})