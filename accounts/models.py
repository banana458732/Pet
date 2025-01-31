import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_set')

    post_code = models.CharField(
        verbose_name='郵便番号',
        max_length=7,
        blank=False,
        null=False,
    )

    phone_number = models.CharField(
        verbose_name='電話番号',
        max_length=15,
        blank=False,
        null=False,
        validators=[RegexValidator(r'^[0-9]{10,11}$', '電話番号は半角数字のみで、10,11桁までにしてください。')],

    )

    address1 = models.CharField(
        verbose_name='都道府県 市区町村', max_length=40, blank=False, null=False
    )

    street_address = models.CharField(
        verbose_name='番地', max_length=6, blank=True, null=False
    )

    address2 = models.CharField(
        verbose_name='建物名', max_length=40, blank=True, null=True
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

    # 郵便番号のハイフン付き表示
    def formatted_post_code(self):
        """郵便番号をハイフン付きで表示する"""
        return f"{self.post_code[:3]}-{self.post_code[3:]}" if self.post_code else ""

    def formatted_phone_number(self):
        """電話番号をハイフン付きで返す"""
        phone_number = self.phone_number

        # 入力からハイフンと小数点を削除
        phone_number = phone_number.replace("-", "").replace(".", "")

        # フリーダイヤル（0120-xxx-xxx）: 10桁
        if len(phone_number) == 10 and phone_number.startswith("0120"):
            return f"{phone_number[:4]}-{phone_number[4:7]}-{phone_number[7:]}"

        # 固定電話（例: 026-267-3353など）: 10桁
        elif len(phone_number) == 10:
            return f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"

        # 11桁の番号（携帯電話やその他）: 11桁
        elif len(phone_number) == 11:
            return f"{phone_number[:3]}-{phone_number[3:7]}-{phone_number[7:]}"

        # それ以外はそのまま返す
        return phone_number
