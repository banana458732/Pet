from django.db import models


class Pet(models.Model):
    TYPE_CHOICES = [
        ('dog', '犬'),
        ('cat', '猫'),
    ]

    SIZE_CHOICES = [
        ('large', '大型'),
        ('medium', '中型'),
        ('small', '小型'),
    ]

    id = models.IntegerField(primary_key=True)  # 明示的にIDフィールドを定義
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='unknown')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='unknown')
    color = models.CharField(max_length=100, default='', blank=True)
    age = models.IntegerField()
    image = models.ImageField(upload_to='pets/', null=True, blank=True)  # 画像フィールドを追加

    def __str__(self):
        return f'{self.type} - {self.size} - {self.color} - {self.age}歳'


class Survey(models.Model):
    # 例：アンケートで収集する情報
    pet_type = models.CharField(max_length=10, choices=[('dog', '犬'), ('cat', '猫')])
    size = models.CharField(max_length=10, choices=[('small', '小型'), ('medium', '中型'), ('large', '大型')])
    age = models.IntegerField()

    def __str__(self):
        return f"{self.pet_type} - {self.size} - {self.age}"