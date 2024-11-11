from django.urls import path
from . import views
from .views import index

app_name = 'Survey'

urlpatterns = [
    path('survey/', views.IndexView.as_view(), name='pet_survey'),
    path('', index, name='index'),
]
