from django.db import models
from django.db.models.signals import pre_delete  # 追加
from django.dispatch import receiver  # 追加
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import os
import pandas as pd
import re

# 現在のスクリプトファイルのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# 1つ上の階層のディレクトリパスを取得
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# 1つ上の階層にあるファイルのパスを作成
file_path = os.path.join(parent_dir, "pets_data.csv")

CSV_FILE_PATH = file_path


class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    TYPE_CHOICES = [
        ('犬', '犬'),
        ('猫', '猫'),
    ]
    SIZE_CHOICES = [
        ('大型', '大型'),
        ('中型', '中型'),
        ('小型', '小型'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='', verbose_name="種類")
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='', verbose_name="サイズ")
    color = models.CharField(max_length=100, default='', verbose_name="色")
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="歳"
    )
    kinds = models.CharField(max_length=100, default='', verbose_name="種別")
    disease = models.CharField(max_length=100, null=True, blank=True, default='', verbose_name="病気")
    personality = models.CharField(max_length=500, null=False, default='', verbose_name="性格")
    sex = models.CharField(
        max_length=10,
        choices=[('オス', 'オス'), ('メス', 'メス')],
        default='', verbose_name="性別"
    )
    post_code = models.CharField(
        max_length=7,
        blank=False,
        null=False,
        verbose_name="郵便番号",
        default=''
    )
    address = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="住所",
        default=''
    )
    phone_number = models.CharField(
        max_length=11,
        blank=False,
        null=True,
        validators=[RegexValidator(r'^[0-9]{10,11}$', '電話番号は半角数字のみで、10,11桁までにしてください。')],
        verbose_name="電話番号"
    )
    location = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="保護場所",
        default=''
    )

    # 保存前に小数点とハイフンを取り除く
    def save(self, *args, **kwargs):
        # 小数点とハイフンを削除
        if self.phone_number:
            self.phone_number = self.phone_number.replace('-', '').replace('.', '')
        if self.post_code:
            self.post_code = self.post_code.replace('.', '')
        super().save(*args, **kwargs)

    # フォーマット済み郵便番号を返すメソッド
    def formatted_post_code(self):
        """郵便番号をハイフン付きで返す"""
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

    def __str__(self):
        return f"{self.id} - {self.type} - {self.sex} - {self.age}歳"


class PhoneNumber(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^[0-9]{10,15}$', '電話番号は半角数字のみで、10～15桁にしてください。')],
        verbose_name="電話番号"
    )

    def __str__(self):
        return self.number


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時を追加

    def __str__(self):
        return f"Image for {self.pet.id}"


@receiver(pre_delete, sender=Pet)
def delete_pet_images(sender, instance, **kwargs):
    for pet_image in instance.images.all():
        if pet_image.image:
            pet_image.image.delete(save=False)  # ファイルを削除
        if pet_image.image and os.path.isfile(pet_image.image.path):
            os.remove(pet_image.image.path)

    # CSVファイルからペット情報を削除
    if os.path.exists(CSV_FILE_PATH):
        data = pd.read_csv(CSV_FILE_PATH)
        data = data[data['id'] != instance.pk]  # 該当する行を削除
        data.to_csv(CSV_FILE_PATH, index=False)


class Survey(models.Model):
    pet_type = models.CharField(max_length=10, choices=[('犬', '犬'), ('猫', '猫')])
    size = models.CharField(max_length=10, choices=[('小型', '小型'), ('中型', '中型'), ('大型', '大型')])
    age = models.IntegerField()

    def __str__(self):
        return f"{self.pet_type} - {self.size} - {self.age}"
