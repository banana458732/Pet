from django.db import models
from django.db.models.signals import pre_delete  # 追加
from django.dispatch import receiver  # 追加
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import os
import pandas as pd

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

    phone_number = models.CharField(
        max_length=15,
        blank=False,
        null=True,
        validators=[RegexValidator(r'^[0-9]{10,15}$', '電話番号は半角数字のみで、10～15桁にしてください。')],
        verbose_name="電話番号"
    )

    def __str__(self):
        return f'{self.type} - {self.size} - {self.color} - {self.age}歳'


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
