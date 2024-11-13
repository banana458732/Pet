from django.db import models  # type: ignore


class SurveyResult(models.Model):
    pet_type = models.CharField(max_length=20)  # ペットの種類
    size = models.CharField(max_length=20, blank=True)  # サイズ
    color = models.CharField(max_length=20, blank=True)  # 色
    age = models.CharField(max_length=20, blank=True)  # 年齢
    living_environment = models.CharField(max_length=255, blank=True)  # 飼育環境
    pet_personality = models.CharField(max_length=255, blank=True)  # 性格
    activity_level = models.CharField(max_length=255, blank=True, default="")  # 活動レベル
    pet_size_preference = models.CharField(max_length=255, blank=True)  # サイズの希望
    additional_requests = models.TextField(blank=True)  # その他の希望

    def __str__(self):
        return f"SurveyResult({self.pet_type}, {self.activity_level})"
