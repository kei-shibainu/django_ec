import random, string
from django.db import models

class PromotionCode(models.Model):

    code = models.CharField(primary_key=True, max_length=7)
    discount = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'promotion_codes'

    @staticmethod
    def create_code():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    
    @staticmethod
    def create_discount():
        return random.randint(100, 1000)

    @classmethod
    def create_promotion_code(cls):
        code = cls.create_code()
        discount = cls.create_discount()
        PromotionCode.objects.create(code=code, discount=discount)
        return code, discount

    def __str__(self):
        return self.code
