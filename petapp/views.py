from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Pet, PetImage
from .forms import PetCreateForm, PetImageFormSet, PetUpdateForm
from django.urls import reverse_lazy
from django.conf import settings
import os
import uuid
from django.core.exceptions import ValidationError


class PetListView(ListView):
    model = Pet
    template_name = 'petapp/pet_list.html'


def pet_create_view(request):
    pet_form = PetCreateForm()
    # 既存の画像を表示しないようにする
    photo_formset = PetImageFormSet(queryset=PetImage.objects.none())

    error_messages = []

    if request.method == 'POST':
        pet_form = PetCreateForm(request.POST)
        photo_formset = PetImageFormSet(request.POST, request.FILES)

        if pet_form.is_valid() and photo_formset.is_valid():
            try:
                pet = pet_form.save()
                for form in photo_formset:
                    if form.is_valid():
                        pet_image = form.save(commit=False)
                        pet_image.pet = pet

                        image = form.cleaned_data.get('image')
                        if image:
                            file_extension = os.path.splitext(image.name)[1]
                            unique_filename = f"uuid_{uuid.uuid4().hex}{file_extension}"
                            pet_image.image.name = unique_filename

                        pet_image.save()

                return redirect('petapp:pet-create-comp', pet_id=pet.id)

            except ValidationError as e:
                error_messages.append(f"Validation error: {str(e)}")

    return render(request, 'petapp/pet_create.html', {
        'form': pet_form,
        'photo_formset': photo_formset,
        'error_messages': error_messages,
    })


def pet_create_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet_images = PetImage.objects.filter(pet=pet)
    return render(request, 'petapp/pet_create_comp.html', {
        'pet': pet,
        'pet_images': pet_images
    })


class PetUpdateView(UpdateView):
    model = Pet
    form_class = PetUpdateForm
    template_name = 'petapp/pet_update.html'

    def get_object(self):
        return get_object_or_404(Pet, id=self.kwargs['pet_id'])

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.save()
        return redirect('petapp:pet-update-comp', pet_id=pet.id)


def pet_update_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'petapp/pet_update_comp.html', {'pet': pet})


class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'petapp/pet_confirm_delete.html'
    success_url = reverse_lazy('petapp:pet-delete-comp')
