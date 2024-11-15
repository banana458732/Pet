import os
import uuid
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pet, PetImage, PhoneNumber
from .forms import PetCreateForm, PetImageFormSet, PetUpdateForm

# 現在のスクリプトファイルのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# 1つ上の階層のディレクトリパスを取得
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# 1つ上の階層にあるファイルのパスを作成
file_path = os.path.join(parent_dir, "pets_data.csv")

# CSVファイルのパスを指定
csv_file_path = file_path

# CSVデータを最初に読み込んでおく
data = pd.read_csv(csv_file_path)

class PetListView(ListView):
    model = Pet
    template_name = 'petapp/pet_list.html'


def pet_create_view(request):
    pet_form = PetCreateForm()
    photo_formset = PetImageFormSet(queryset=PetImage.objects.none())
    error_messages = []

    # CSVデータを最初に読み込んでおく
    data = pd.read_csv(csv_file_path)

    if request.method == 'POST':
        pet_form = PetCreateForm(request.POST)
        photo_formset = PetImageFormSet(request.POST, request.FILES)

        if pet_form.is_valid() and photo_formset.is_valid():
            try:
                # ペット情報の保存
                pet = pet_form.save()

                # 画像の保存
                image_urls = []
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
                            # 画像のURLをリストに追加
                            image_urls.append(pet_image.image.url)

                # 電話番号があれば保存
                phone_number = request.POST.get('phone_number')
                if phone_number:
                    PhoneNumber.objects.create(pet=pet, number=phone_number)

                # ペットデータをCSVに追加
                new_pet_data = {
                    'id': pet.id,
                    'type': pet.type,
                    'size': pet.size,
                    'color': pet.color,
                    'age': pet.age,
                    'syu': pet.syu,
                    'disease': pet.disease,
                    'personality': pet.personality,
                    'sex': pet.sex,
                    'image_urls': ', '.join(image_urls)
                }

                # CSVファイルを再読み込みして新しいデータを追加
                data = pd.read_csv(csv_file_path)
                new_pet_df = pd.DataFrame([new_pet_data])
                data = pd.concat([data, new_pet_df], ignore_index=True)
                data.to_csv(csv_file_path, index=False)

                return redirect('petapp:pet-create-comp', pet_id=pet.id)

            except ValidationError as e:
                error_messages.append(f"Validation error: {str(e)}")

    return render(request, 'petapp/pet_create.html', {
        'form': pet_form,
        'photo_formset': photo_formset,
        'error_messages': error_messages,
        'csv_data': data.head()  # CSVデータを渡す
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

    def delete(self, request, *args, **kwargs):
        pet = self.get_object()
        response = super().delete(request, *args, **kwargs)

        try:
            # CSVファイルを読み込んで指定IDの行を削除
            data = pd.read_csv(csv_file_path)
            data = data[data['id'] != pet.id]
            data.to_csv(csv_file_path, index=False)
        except Exception as e:
            print(f"Error updating CSV file after deleting pet: {str(e)}")

        return response


def index(request):
    return render(request, 'Survey/index.html', {'csv_data': data.head()})
