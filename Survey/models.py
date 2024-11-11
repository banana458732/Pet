from django.db import models


class SurveyResult(models.Model):
    pet_type = models.CharField(max_length=20)
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=20, blank=True)
    age = models.CharField(max_length=20, blank=True)
    living_environment = models.CharField(max_length=255, blank=True)  # 空白を許可
    pet_personality = models.CharField(max_length=255, blank=True)  # 空白を許可
    activity_level = models.CharField(max_length=255, blank=True, default="")  # 空白を許可し、デフォルトを設定
    pet_size_preference = models.CharField(max_length=255, blank=True)  # 空白を許可
    additional_requests = models.TextField(blank=True)  # 空白を許可

    def __str__(self):
        return f"SurveyResult({self.pet_type}, {self.size}, {self.color}, {self.age}, {self.living_environment})"
