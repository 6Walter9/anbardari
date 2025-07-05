from django.urls import path
from . import views

urlpatterns = [
    # آدرس ریشه سایت، ویو home_page را نمایش می‌دهد
    path('', views.home_page, name='home_page'),
]