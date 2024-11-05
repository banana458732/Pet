from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Pet
from .forms import PetCreateForm, PetUpdateForm


class PetListView(ListView):
    model = Pet
    template_name = 'petapp/pet_list.html'


class PetCreateView(CreateView):
    model = Pet
    form_class = PetCreateForm
    template_name = 'petapp/pet_create.html'
    success_url = '/pets/'


class PetUpdateView(UpdateView):
    model = Pet
    form_class = PetUpdateForm
    template_name = 'petapp/pet_update.html'
    success_url = '/pets/'

    def get_object(self):
        # IDを固定するために、オブジェクトを取得する
        return get_object_or_404(Pet, pk=self.kwargs['pk'])


class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'petapp/pet_confirm_delete.html'
    success_url = '/pets/'
