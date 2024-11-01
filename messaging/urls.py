from django.urls import path
from . import views
from .views import index

app_name = 'messaging'


urlpatterns = [
    path('messaging/', views.IndexView.as_view(), name='send_message'),
    path('', index, name='index'),
    path('send/', views.send_message, name='send_message'),
    path('pets/<str:pet_id>/', views.pet_detail, name='pet_detail'),  # ペットの詳細
]
