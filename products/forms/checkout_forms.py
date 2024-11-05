from django import forms
from django.utils import timezone
from django.forms import ValidationError

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

        now = timezone.now()
        current_year = now.year
        current_month = now.month

        if expiration_year < current_year or (expiration_year == current_year and expiration_month < current_month):
            raise ValidationError('クレジットカードの有効期限が過ぎています。')