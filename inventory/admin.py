from django.contrib import admin
# مدل خودمان را از فایل models.py وارد می‌کنیم
from .models import StockEntry

# مدل StockEntry را در پنل ادمین ثبت می‌کنیم
admin.site.register(StockEntry)