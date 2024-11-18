from django.db import models
from django.contrib.auth.models import User  # ユーザーとの関連を持つためにインポート

class SurveyResult(models.Model):
    """アンケート結果のモデル"""
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

class SurveyHistory(models.Model):
    """ユーザーごとの過去のアンケート結果履歴"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_history')  # ユーザーとの関連
    survey_result = models.ForeignKey(SurveyResult, on_delete=models.CASCADE, related_name='survey_histories')  # SurveyResultとの関連
    date_created = models.DateTimeField(auto_now_add=True)  # 履歴の作成日時

    def __str__(self):
        return f"SurveyHistory(user={self.user.username}, date_created={self.date_created})"
