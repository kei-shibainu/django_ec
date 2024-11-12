from django import forms
from django.utils import timezone
from django.forms import ValidationError
from datetime import datetime

from products.models.customers import Customer

class CheckOut(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def clean(self) -> None:
        expiration_year = self.cleaned_data.get('expiration_year')
        expiration_month = self.cleaned_data.get('expiration_month')

        if expiration_year is None or expiration_month is None:
            raise ValidationError('有効期限を正しく設定してください。')
        localtime = timezone.localtime(timezone.now()).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        try:
            expiration_date = timezone.make_aware(datetime(int(expiration_year), int(expiration_month), 1), timezone.get_current_timezone())
            if expiration_date < localtime: 
                raise ValidationError('クレジットカードの有効期限が過ぎています。')
        except ValueError:
            raise ValidationError('有効期限の月、または年が無効です。')
