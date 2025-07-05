from django.shortcuts import render, redirect
from .forms import StockEntryForm
from django.views.generic import ListView
from .models import StockEntry
from django.db.models import Q
#from django.shortcuts import render, redirect
from .forms import StockEntryForm
from django.http import JsonResponse
from django.template.loader import render_to_string
import json

def add_stock_entry(request):
    if request.method == 'POST':
        form = StockEntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save()
            # رندر کردن ردیف جدید جدول برای ارسال به فرانت‌اند
            html = render_to_string(
                template_name='inventory/_entry_table_rows.html',
                context={'entries': [new_entry]} # فقط آیتم جدید را در یک لیست قرار می‌دهیم
            )
            return JsonResponse({'status': 'success', 'html_from_view': html})
        else:
            # برگرداندن خطاها در قالب JSON
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=405)

class InventoryDashboardView(ListView):
    model = StockEntry
    template_name = 'inventory/inventory_dashboard.html'
    context_object_name = 'entries'
    paginate_by = 10 

    def get_queryset(self):
        # فقط مواردی را نشان بده که حذف نشده‌اند
        #return StockEntry.objects.filter(deleted__isnull=True).order_by('-tarikh', '-id')
        queryset = StockEntry.objects.filter(deleted__isnull=True).order_by('-tarikh', '-id')
    
    
        search_query = self.request.GET.get('q')
        if search_query:
                # اگر عبارتی برای جستجو وجود داشت، لیست را فیلتر می‌کنیم
            queryset = queryset.filter(
                Q(sharh__icontains=search_query) |
                Q(shomare_faktor__icontains=search_query) |
                Q(anbar__icontains=search_query) |
                Q(taahod__icontains=search_query) |
                Q(mahale_tamin__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_form'] = StockEntryForm()
        return context
def search_entries_api(request):
    queryset = StockEntry.objects.filter(deleted__isnull=True).order_by('-tarikh', '-id')
    
    search_query = request.GET.get('q')
    taahod_filter = request.GET.get('taahod')
    search_in_field = request.GET.get('search_in') # فیلد جدید را از درخواست می‌خوانیم

    if search_query:
        if search_in_field == 'sharh':
            queryset = queryset.filter(sharh__icontains=search_query)
        elif search_in_field == 'shomare_faktor':
            queryset = queryset.filter(shomare_faktor__icontains=search_query)
        else: # حالت پیش‌فرض یا اگر 'all' انتخاب شده باشد
            queryset = queryset.filter(
                Q(sharh__icontains=search_query) |
                Q(shomare_faktor__icontains=search_query)
            )
    
    if taahod_filter:
        queryset = queryset.filter(taahod=taahod_filter)
        
    html = render_to_string(
        template_name='inventory/_entry_table_rows.html',
        context={'entries': queryset}
    )
    
    data_dict = {"html_from_view": html}
    
    return JsonResponse(data=data_dict, safe=False)

def delete_entries_api(request):
    if request.method == 'POST':
        try:
            # خواندن لیست آیدی‌ها از بدنه درخواست
            data = json.loads(request.body)
            ids_to_delete = data.get('ids', [])
            
            if not ids_to_delete:
                return JsonResponse({'status': 'error', 'message': 'هیچ آیتمی انتخاب نشده است.'}, status=400)

            # پیدا کردن و حذف (نرم) آیتم‌های مورد نظر
            StockEntry.objects.filter(id__in=ids_to_delete).delete()
            
            return JsonResponse({'status': 'success', 'message': 'آیتم‌های انتخابی با موفقیت حذف شدند.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=405)


def entry_edit_api(request, pk):
    try:
        entry = StockEntry.objects.get(pk=pk, deleted__isnull=True)
    except StockEntry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'آیتم یافت نشد.'}, status=404)

    if request.method == 'GET':
        # تبدیل اطلاعات مدل به یک دیکشنری برای ارسال به فرانت‌اند
        data = {
            'tarikh': entry.tarikh,
            'sharh': entry.sharh,
            'vahed': entry.vahed,
            'meghdar': entry.meghdar,
            'shomare_faktor': entry.shomare_faktor,
            'fi': entry.fi,
            'takhfif': entry.takhfif,
            'vaziat_mali': entry.vaziat_mali,
            'taahod': entry.taahod,
            'anbar': entry.anbar,
            'mahale_estefade': entry.mahale_estefade,
            'tozihat': entry.tozihat,
            'mahale_tamin': entry.mahale_tamin,
            # برای فیلدهای عکس، فقط آدرسشان را می‌فرستیم
            'tasvir_faktor_url': entry.tasvir_faktor.url if entry.tasvir_faktor else '',
            'tasvir_resid_url': entry.tasvir_resid.url if entry.tasvir_resid else '',
        }
        return JsonResponse({'status': 'success', 'data': data})

    elif request.method == 'POST':
        # برای به‌روزرسانی، فرم را با اطلاعات جدید و نمونه موجود پر می‌کنیم
        form = StockEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            updated_entry = form.save()
            # رندر کردن ردیف به‌روز شده برای جایگزینی در جدول
            html = render_to_string(
                template_name='inventory/_entry_table_rows.html',
                context={'entries': [updated_entry]}
            )
            return JsonResponse({'status': 'success', 'html_from_view': html, 'id': updated_entry.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})