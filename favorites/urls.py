# favorites/urls.py
from django.urls import path
from . import views

app_name = 'favorites'  # 名前空間を設定

urlpatterns = [
    path('add/<int:pet_id>/', views.add_favorite, name='add'),  # お気に入り追加
    path('remove/<int:pet_id>/', views.remove_favorite, name='remove'),  # お気に入り削除
]
