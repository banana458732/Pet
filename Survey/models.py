from django.db import models
from django.contrib.auth.models import User


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


class SurveyHistory(models.Model):
    """ユーザーごとの過去のアンケート結果履歴"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_history')  # ユーザーとの関連
    survey_result = models.ForeignKey('SurveyResult', on_delete=models.CASCADE, related_name='survey_histories')  # SurveyResultとの関連
    date_created = models.DateTimeField(auto_now_add=True)  # 履歴の作成日時

    # 修正した部分：デフォルト値を設定
    matched_pet = models.ForeignKey('petapp.Pet', on_delete=models.CASCADE, related_name='survey_histories', default=1)  # デフォルト値（Petインスタンス）

    def __str__(self):
        return f"Survey by {self.user.username} on {self.date_created}"