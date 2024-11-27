from django.urls import path
from . import views

app_name = 'messaging'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('send/', views.send_message, name='send_message'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),  # ペットの詳細
    path('pet/<int:pet_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
]
