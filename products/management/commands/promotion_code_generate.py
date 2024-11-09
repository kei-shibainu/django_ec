from typing import Any
from django.core.management.base import BaseCommand

from products.models.promotion_codes import PromotionCode

class Command(BaseCommand):
    help = 'ランダムな10個のプロモーションコードを作成します。'

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            for _ in range(10):
                code, discount = PromotionCode.create_promotion_code()
                self.stdout.write(self.style.SUCCESS(f'code:{code}, discount:{discount}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))