# admin.py
from django.contrib import admin
from .models import SurveyResult

admin.site.register(SurveyResult)  # モデルを管理画面に登録
