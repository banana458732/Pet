# survey/urls.py
from django.urls import path
from . import views

app_name = 'survey'  # 名前空間の設定

urlpatterns = [
    path('survey/', views.IndexView.as_view(), name='pet_survey'),
    path('', views.index, name='index'),
    path('history/<int:id>/', views.history_detail, name='history_detail'),  # 履歴詳細ページ
]
