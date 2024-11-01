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
from . import views

urlpatterns = [
    path('', views.PetListView.as_view(), name='pet-list'),  # 'pets/' はプロジェクトのurls.pyで追加されるため不要
    path('new/', views.PetCreateView.as_view(), name='pet-create'),
    path('<int:pk>/update/', views.PetUpdateView.as_view(), name='pet-update'),
    path('<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet-delete'),
]
