from django.shortcuts import render

def home_page(request):
    # این ویو فعلا هیچ منطق خاصی ندارد و فقط یک صفحه را نمایش می‌دهد
    return render(request, 'core/home.html')