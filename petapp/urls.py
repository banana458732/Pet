from django.urls import path
from .views import PetListView, PetUpdateView, PetDeleteView, pet_create_view, pet_create_comp_view, pet_update_comp_view
from django.views.generic import TemplateView
from . import views  # views.py からインポート


app_name = 'petapp'

urlpatterns = [
    path('', PetListView.as_view(), name='pet-list'),
    path('new/', pet_create_view, name='pet-create'),
    path('complete/<int:pet_id>/', pet_create_comp_view, name='pet-create-comp'),
    path('<int:pet_id>/update/', PetUpdateView.as_view(), name='pet-update'),
    path('updatecomp/<int:pet_id>/', pet_update_comp_view, name='pet-update-comp'),
    path('<int:pk>/delete/', PetDeleteView.as_view(), name='pet-delete'),
    path('deletecomp/', TemplateView.as_view(template_name='petapp/pet_delete_comp.html'), name='pet-delete-comp'),
]
