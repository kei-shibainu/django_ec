from django.db import models
import uuid

def file_upload_path(instance, filename):
    return f'uploads/{instance.id}/{filename}'
# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="商品名")
    description = models.TextField(null=True, blank=True, verbose_name="説明")
    price = models.PositiveIntegerField(default=0, verbose_name="価格")
    stock = models.PositiveIntegerField(default=0, verbose_name="在庫数")
    sold_quantity = models.PositiveIntegerField(default=0, editable=False, verbose_name="販売数")
    review = models.PositiveIntegerField(default=0, editable=False, verbose_name="レビュー")
    discount_rate = models.PositiveIntegerField(default=0, verbose_name="割引率")
    discount_price = models.PositiveIntegerField(default=0, editable=False, verbose_name="割引価格")
    image = models.ImageField(default='', upload_to=file_upload_path, blank=True, verbose_name="画像")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name="削除フラグ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    def save(self, *args, **kwargs):
        if 0 < self.discount_rate:
            discount = (self.price * self.discount_rate) / 100
            self.discount_price = self.price - discount
        else:
            self.discount_price = self.price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'products'