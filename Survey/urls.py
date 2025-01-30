from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.pet_survey, name='pet_survey'),
    path('results/', views.results, name='results'),   # アンケート
]
