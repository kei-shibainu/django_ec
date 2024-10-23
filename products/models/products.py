from django.db import models
import uuid

def file_upload_path(instance, filename):
    return f'static/uploads/{instance.id}/{filename}'

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)
    review = models.PositiveIntegerField(default=0)
    discount_rate = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0, editable=False)
    image = models.ImageField(default='', upload_to=file_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if 0 < self.discount_rate:
            discount = (self.price * self.discount_rate) / 100
            self.discount_price = self.price - discount
        else:
            self.discount_price = self.price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name