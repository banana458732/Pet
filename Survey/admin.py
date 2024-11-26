# admin.py
from django.contrib import admin
from .models import SurveyResult, MatchingHistory

admin.site.register(SurveyResult)  # モデルを管理画面に登録
admin.site.register(MatchingHistory)
