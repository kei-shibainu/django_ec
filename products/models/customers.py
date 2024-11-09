import uuid
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Prefecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, verbose_name='名')
    last_name = models.CharField(max_length=50, verbose_name='姓')
    user_name = models.CharField(max_length=50, verbose_name='ユーザー名')
    email = models.EmailField(max_length=254, verbose_name='メールアドレス')
    zip = models.CharField(verbose_name='郵便番号', validators=[
        RegexValidator(regex=r'^\d{3}-?\d{4}$',
        message="郵便番号は「XXX-XXXX」または「XXXXXXX」の形式で入力してください。",
        )
    ])
    prefecture = models.ForeignKey(Prefecture, on_delete=models.PROTECT, verbose_name='都道府県', related_name='customers')
    address = models.CharField(max_length=255, verbose_name='住所')
    address2 = models.CharField(max_length=255, blank=True, default='', verbose_name='建物名(任意)')
    credit_name = models.CharField(max_length=100, verbose_name='カード名義人', validators=[
        RegexValidator(
            regex=r'^[a-zA-Z\s\']+$',
            message='カード名義人は半角英字、またはスペース、アポストロフィで入力してください。'
        )
    ])
    credit_number = models.CharField(verbose_name='クレジットカード番号', validators=[
        RegexValidator(
            regex=r'^\d{16}$',
            message='クレジットカード番号は16桁の数字で入力してください。'
        )
    ])
    expiration_month = models.IntegerField(verbose_name='有効期限(月)', validators=[
        MinValueValidator(1),
        MaxValueValidator(12),
    ])
    expiration_year = models.IntegerField(verbose_name='有効期限(年)')
    credit_cvv = models.CharField(verbose_name='CVV', validators=[
        RegexValidator(
            regex=r'\d{3}$',
            message='CVVは3桁の数字で入力してください。'
        )
    ])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        db_table = 'customers'