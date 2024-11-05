from django.urls import path
from . import views
from .views import index

app_name = 'messaging'


urlpatterns = [
    path('', views.IndexView.as_view(), name='Index'),
    path('', index, name='index'),
    path('send/', views.send_message, name='send_message'),
    path('pet/<str:pet_id>/', views.pet_detail, name='pet_detail'),  # ペットの詳細
]
