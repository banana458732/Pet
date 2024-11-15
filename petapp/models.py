from django.db import models
from django.db.models.signals import pre_delete  # 追加
from django.dispatch import receiver  # 追加
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import os
import pandas as pd

# CSV ファイルのパスを指定
CSV_FILE_PATH = 'C:\\Users\\t_koitabashi\\Desktop\\卒業制作\\Pet\\pets_data.csv'


class Pet(models.Model):
    TYPE_CHOICES = [
        ('犬', '犬'),
        ('猫', '猫'),
    ]

    SIZE_CHOICES = [
        ('大型', '大型'),
        ('中型', '中型'),
        ('小型', '小型'),
    ]

    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='')
    color = models.CharField(max_length=100, default='')
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)]
    )
    syu = models.CharField(max_length=100, default='')
    disease = models.CharField(max_length=100, null=True, blank=True, default='')
    personality = models.CharField(max_length=500, null=False, default='')
    sex = models.CharField(
        max_length=10,
        choices=[('男の子', '男の子'), ('女の子', '女の子')],
        default=''
    )

    phone_number = models.CharField(
        max_length=15,
        blank=False,
        null=True,
        validators=[RegexValidator(r'^[0-9]{10,15}$', '電話番号は半角数字のみで、10～15桁にしてください。')]
    )

    def __str__(self):
        return f'{self.type} - {self.size} - {self.color} - {self.age}歳'


class PhoneNumber(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^[0-9]{10,15}$', '電話番号は半角数字のみで、10～15桁にしてください。')]
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
    # 関連する画像を削除
    for pet_image in instance.images.all():
        if pet_image.image and os.path.isfile(pet_image.image.path):
            os.remove(pet_image.image.path)

    # CSVファイルからペット情報を削除
    if os.path.exists(CSV_FILE_PATH):
        data = pd.read_csv(CSV_FILE_PATH)
        data = data[data['id'] != instance.id]  # 該当する行を削除
        data.to_csv(CSV_FILE_PATH, index=False)


class Survey(models.Model):
    pet_type = models.CharField(max_length=10, choices=[('犬', '犬'), ('猫', '猫')])
    size = models.CharField(max_length=10, choices=[('小型', '小型'), ('中型', '中型'), ('大型', '大型')])
    age = models.IntegerField()

    def __str__(self):
        return f"{self.pet_type} - {self.size} - {self.age}"
