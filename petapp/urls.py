# petapp/urls.py
# from django.urls import path
# from .views import PetListView, PetCreateView, PetUpdateView, PetDeleteView

# urlpatterns = [
#     path('pets/', PetListView.as_view(), name='pet-list'),
#     path('pets/new/', PetCreateView.as_view(), name='pet-create'),
#     path('pets/<int:pk>/update/', PetUpdateView.as_view(), name='pet-update'),
#     path('pets/<int:pk>/delete/', PetDeleteView.as_view(), name='pet-delete'),
# ]

# petapp/urls.py
# from django.urls import path
# from .views import PetListView, PetCreateView, PetUpdateView, PetDeleteView

# urlpatterns = [
#     path('', PetListView.as_view(), name='pet-list'),  # ペットリスト
#     path('new/', PetCreateView.as_view(), name='pet-create'),  # 新規作成
#     path('<int:pk>/update/', PetUpdateView.as_view(), name='pet-update'),  # 更新
#     path('<int:pk>/delete/', PetDeleteView.as_view(), name='pet-delete'),  # 削除
# ]

# ^^^^^^^^^^^^^^

# petapp/urls.py
# from django.urls import path
# from .views import PetListView, PetCreateView, PetUpdateView, PetDeleteView

# urlpatterns = [
#     path('', PetListView.as_view(), name='pet-list'),
#     path('new/', PetCreateView.as_view(), name='pet-create'),
#     path('pets/<int:pk>/update/', PetUpdateView.as_view(), name='pet-update'),
#     path('pets/<int:pk>/delete/', PetDeleteView.as_view(), name='pet-delete'),
# ]

from django.urls import path
from .views import PetListView, PetCreateView, PetUpdateView, PetDeleteView

app_name = 'petapp'  # アプリケーション名前空間を追加

urlpatterns = [
    path('', PetListView.as_view(), name='pet-list'),                   # 一覧ページ
    path('new/', PetCreateView.as_view(), name='pet-create'),           # 新規登録ページ
    path('<int:pk>/update/', PetUpdateView.as_view(), name='pet-update'),  # 更新ページ
    path('<int:pk>/delete/', PetDeleteView.as_view(), name='pet-delete'),  # 削除ページ
]
