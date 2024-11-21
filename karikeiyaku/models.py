from django.db import models
from django.contrib.auth.models import User
from petapp.models import Pet

class Karikeiyaku(models.Model):
    # ユーザーとペットを紐づけ
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="ペット")

    # 価格は必須ではないので、null=True, blank=Trueを追加
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="価格")
    
    # 契約終了日は必須でないので、null=True, blank=Trueを追加
    end_date = models.DateField(null=True, blank=True, verbose_name="契約終了日")
    
    # 飼育に必要なスペースがあるかの確認
    has_appropriate_space = models.BooleanField(default=False, verbose_name="適切なスペースがある")
    
    # 責任を理解しているかの確認
    understands_responsibility = models.BooleanField(default=False, verbose_name="責任を理解している")
    
    # ステータス（仮契約中、キャンセルなど）
    status = models.CharField(max_length=50, choices=[
        ('仮契約中', '仮契約中'),
        ('キャンセル', 'キャンセル'),
        ('正式契約済', '正式契約済')
    ], default='仮契約中', verbose_name="ステータス")

    # キャンセルポリシーを追加
    cancellation_policy = models.TextField(null=True, blank=True, verbose_name="キャンセルポリシー")
    
    # 病歴フィールド（ペットの病歴があれば表示）
    disease = models.CharField(max_length=255, null=True, blank=True, verbose_name="病歴")

    # 作成日時（自動で保存）
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    class Meta:
        app_label = 'karikeiyaku'

    def __str__(self):
        return f"{self.pet}の仮契約"
