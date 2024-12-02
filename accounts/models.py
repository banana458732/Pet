from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from petapp.models import Pet


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_set')

    address = models.CharField(
        verbose_name='住所',
        max_length=30,
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        verbose_name='電話番号',
        max_length=15,
        null=True,
        blank=True
    )

    contract_pets = models.ManyToManyField(
        'petapp.Pet',  # アプリ名.petモデル
        blank=True,
        related_name='contracted_users',
        verbose_name='仮契約したペット'
    )

    # プロフィール画像のフィールド
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        default='profile_images/default.jpg'  # デフォルト画像
    )

    def delete_old_image(self):
        """古い画像をストレージから削除する"""
        # 古い画像のパスを取得
        if self.profile_image and self.profile_image.name != 'profile_images/default.jpg':
            old_image_path = os.path.join(settings.MEDIA_ROOT, self.profile_image.name)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

    def save(self, *args, **kwargs):
        # インスタンスが既存の場合、古い画像を削除
        try:
            old_instance = CustomUser.objects.get(pk=self.pk)
            if old_instance.profile_image != self.profile_image:
                old_instance.delete_old_image()
        except CustomUser.DoesNotExist:
            pass  # 新規作成時は削除処理をスキップ

        super().save(*args, **kwargs)
