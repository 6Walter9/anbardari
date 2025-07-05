from django import forms
from .models import StockEntry

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        # لیست فیلدهایی که می‌خواهیم در فرم نمایش داده شوند
        fields = [
            'tarikh', 'sharh', 'vahed', 'meghdar', 'shomare_faktor', 
            'fi', 'takhfif', 'vaziat_mali', 'taahod', 'anbar', 
            'mahale_estefade', 'tozihat', 'mahale_tamin', 
            'tasvir_faktor', 'tasvir_resid'
        ]
        # ما فیلد 'mablagh' را اینجا نیاوردیم چون آن را خودکار محاسبه می‌کنیم

    def save(self, commit=True):
        # متد save را بازنویسی می‌کنیم تا مبلغ کل را محاسبه کنیم
        instance = super().save(commit=False)

        # محاسبه مبلغ کل
        meghdar = self.cleaned_data.get('meghdar', 0)
        fi = self.cleaned_data.get('fi', 0)
        takhfif = self.cleaned_data.get('takhfif', 0)

        mablagh_bedone_takhfif = meghdar * fi
        mablagh_takhfif = mablagh_bedone_takhfif * (takhfif / 100)
        instance.mablagh = mablagh_bedone_takhfif - mablagh_takhfif

        if commit:
            instance.save()
        return instance