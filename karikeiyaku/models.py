from django.db import models
from django.conf import settings
from petapp.models import Pet
from django.conf import settings


class Karikeiyaku(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="ユーザー")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="ペット")
    end_date = models.DateField(null=True, blank=True, verbose_name="契約終了日")
    created_at = models.DateField(auto_now_add=True, verbose_name="作成日時")
    status = models.CharField(
        max_length=50,
        choices=[
            ('仮契約中', '仮契約中'),
            ('キャンセル', 'キャンセル'),
            ('仮契約済', '仮契約済'),
            ('契約済み', '契約済み')  # 契約済みを追加
        ],
        default='仮契約中', verbose_name="ステータス",
        null=True, blank=True
    )

    class Meta:
        app_label = 'karikeiyaku'

    def __str__(self):
        return f"{self.pet}の仮契約"