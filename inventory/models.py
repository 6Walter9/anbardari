from django.db import models
from django.utils import timezone
from safedelete.models import SafeDeleteModel

# برای کار با تاریخ شمسی، بعداً این کتابخانه را نصب و فعال می‌کنیم
# from django_jalali.db import models as jmodels


# تعریف گزینه‌های ثابت برای فیلد "تعهد"
TAAHOD_CHOICES = [
    ('علوی', 'علوی'),
    ('بهزادی', 'بهزادی'),
    ('رحمانی', 'رحمانی'),
    ('پرداختی', 'پرداختی'),
]

# تعریف گزینه‌های ثابت برای فیلد "وضعیت مالی"
FINANCIAL_STATUS_CHOICES = [
    ('تسویه', 'تسویه'),
    ('مانده', 'مانده'),
]


class StockEntry(SafeDeleteModel):
    # ردیف به صورت خودکار توسط جنگو با نام id ساخته می‌شود
    
    # ما از تاریخ میلادی جنگو استفاده می‌کنیم ولی در نمایش به کاربر شمسی نشان خواهیم داد
    tarikh = models.DateField(default=timezone.now, verbose_name="تاریخ")
    sharh = models.CharField(max_length=300, verbose_name="شرح کالا")
    vahed = models.CharField(max_length=50, verbose_name="واحد")
    meghdar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مقدار")
    
    shomare_faktor = models.CharField(max_length=100, blank=True, null=True, verbose_name="شماره فاکتور")
    fi = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="فی (ریال)")
    takhfif = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="تخفیف (درصدی)")
    
    # این فیلد را به صورت خودکار محاسبه و ذخیره خواهیم کرد
    mablagh = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="مبلغ کل (ریال)")
    
    vaziat_mali = models.CharField(max_length=50, choices=FINANCIAL_STATUS_CHOICES, verbose_name="وضعیت مالی")
    taahod = models.CharField(max_length=100, choices=TAAHOD_CHOICES, verbose_name="تعهد")
    anbar = models.CharField(max_length=100, verbose_name="انبار")
    
    mahale_estefade = models.CharField(max_length=200, blank=True, null=True, verbose_name="محل استفاده")
    tozihat = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    mahale_tamin = models.CharField(max_length=200, blank=True, null=True, verbose_name="محل تامین")
    
    tasvir_faktor = models.ImageField(upload_to='invoices/', blank=True, null=True, verbose_name="تصویر فاکتور")
    tasvir_resid = models.ImageField(upload_to='receipts/', blank=True, null=True, verbose_name="تصویر رسید تحویل")

    class Meta:
        verbose_name = "سند ورود"
        verbose_name_plural = "اسناد ورود"
        ordering = ['-tarikh', '-id'] # رکوردهای جدیدتر بالاتر نمایش داده می‌شوند

    def __str__(self):
        return f"{self.sharh} - {self.tarikh}"