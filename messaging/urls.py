from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('send/', views.send_message, name='send_message'),
    path('pets/<str:pet_id>/', views.pet_detail, name='pet_detail'),  # ペットの詳細
]
