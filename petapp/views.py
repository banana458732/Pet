from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Pet, PetImage
from .forms import PetCreateForm, PetImageForm, PetUpdateForm, PetImageFormSet
from django.urls import reverse_lazy


class PetListView(ListView):
    model = Pet
    template_name = 'petapp/pet_list.html'


def pet_create_view(request):
    if request.method == 'POST':
        pet_form = PetCreateForm(request.POST)
        photo_formset = PetImageFormSet(request.POST, request.FILES, queryset=PetImage.objects.none())

        # 各フォームのラベルを設定
        for i, form in enumerate(photo_formset):
            form.fields['image'].label = f'写真{i+1}'

        if pet_form.is_valid() and photo_formset.is_valid():
            pet = pet_form.save()
            # 写真のフォームセットからデータを保存
            for form in photo_formset:
                if form.is_valid() and form.cleaned_data.get('image'):  # バリデーションが通った場合のみcleaned_dataを使う
                    photo = form.save(commit=False)
                    photo.pet = pet
                    photo.save()

            return redirect('petapp:pet-create-comp', pet_id=pet.id)
        else:
            print("Pet form errors:", pet_form.errors)
            print("写真が入っていません:", photo_formset.errors)
    else:
        pet_form = PetCreateForm()
        photo_formset = PetImageFormSet(queryset=PetImage.objects.none())

        for i, form in enumerate(photo_formset):
            form.fields['image'].label = f'写真{i+1}'

    return render(request, 'petapp/pet_create.html', {
        'form': pet_form,
        'photo_formset': photo_formset,
    })


def pet_create_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'petapp/pet_create_comp.html', {'pet': pet})


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
