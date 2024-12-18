from django.db import models
from django.contrib.auth.models import User
from petapp.models import Pet  # Pet モデルをインポート


class SurveyResult(models.Model):
    """アンケート結果を格納するモデル"""
    pet_type = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=255, blank=True)
    pet_personality = models.CharField(max_length=255, blank=True)
    activity_level = models.CharField(max_length=255, blank=True)
    pet_size_preference = models.CharField(max_length=255, blank=True)
    additional_requests = models.TextField(blank=True)
    kinds = models.CharField(max_length=255, blank=True)
    disease = models.CharField(max_length=255, blank=True, default='')
    sex = models.CharField(max_length=255, blank=True)
    image_urls = models.TextField(blank=True)
    age_range = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.pet_type} - {self.size}"
