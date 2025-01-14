from django.urls import path
from . import views

app_name = 'messaging'


urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),  # ペットの詳細
]
