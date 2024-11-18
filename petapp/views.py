import os
import uuid
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from .models import Pet, PetImage, PhoneNumber
from .forms import PetCreateForm, PetImageFormSet, PetUpdateForm, PetImageForm
from django.forms import modelformset_factory
from django.core.files.storage import default_storage

# CSVファイルのパスを指定
CSV_FILE_PATH = 'C:\\Users\\t_yamanoi\\Documents\\卒業制作\\Pet\\pets_data.csv'

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

# NaNを「なし」に置き換え
data.fillna('なし', inplace=True)


# CSVファイルを読み書きする関数
def read_csv():
    """CSVファイルを読み込んでDataFrameを返す"""
    if os.path.exists(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    else:
        return pd.DataFrame(columns=['id', 'type', 'size', 'color', 'age', 'syu', 'disease', 'personality', 'sex'])


def write_csv(data):
    """DataFrameをCSVファイルに書き込む"""
    data.to_csv(CSV_FILE_PATH, index=False)


# ペットリストのビュー
class PetListView(ListView):
    model = Pet
    template_name = 'petapp/pet_list.html'


def save_image(image):
    """画像を保存して、そのパスまたはURLを返す処理"""
    # 画像を保存するパスを指定
    image_dir = 'media/pet_images/'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)  # ディレクトリが存在しない場合は作成

    image_path = os.path.join(image_dir, image.name)

    # 画像を保存
    with open(image_path, 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)

    return image_path  # 保存した画像のパスを返す

# CSVファイルの読み込み
def read_csv():
    return pd.read_csv(csv_file_path)

# CSVファイルへの書き込み
def write_csv(data):
    data.to_csv(csv_file_path, index=False)


# ペット新規作成ビュー
def pet_create_view(request):
    pet_form = PetCreateForm()
    photo_formset = PetImageFormSet(queryset=PetImage.objects.none())
    error_messages = []

    # CSVデータを最初に読み込んでおく
    data = read_csv()

    # 'id'列が存在しない場合、'id'列を作成
    if 'id' not in data.columns:
        data['id'] = pd.Series(dtype=int)  # 'id'列がない場合は空の整数列を作成
    data.fillna('なし', inplace=True)  # 欠損値を'なし'に埋める

    if request.method == 'POST':
        pet_form = PetCreateForm(request.POST)
        photo_formset = PetImageFormSet(request.POST, request.FILES)

        if pet_form.is_valid() and photo_formset.is_valid():
            try:
                pet = pet_form.save()

                # 画像保存処理
                photo_uploaded = False
                image_urls = []  # 画像URLを格納するリスト

                for form in photo_formset:
                    pet_image = form.save(commit=False)
                    pet_image.pet = pet

                    image = form.cleaned_data.get('image')
                    if image:
                        photo_uploaded = True
                        # ユニークなファイル名を生成
                        unique_filename = f"uuid_{uuid.uuid4().hex}{os.path.splitext(image.name)[1]}"
                        pet_image.image.name = unique_filename
                        pet_image.save()

                        # 画像URLをリストに追加
                        image_url = save_image(image)
                        image_urls.append(image_url)

                # 画像がアップロードされていない場合の処理
                if not photo_uploaded:
                    error_messages.append("少なくとも1つの画像をアップロードしてください。")
                    pet.delete()  # ペット作成を取り消し
                    return render(request, 'petapp/pet_create.html', {
                        'form': pet_form,
                        'photo_formset': photo_formset,
                        'error_messages': error_messages,
                    })

                # 電話番号保存
                phone_number = request.POST.get('phone_number')
                if phone_number:
                    PhoneNumber.objects.create(pet=pet, number=phone_number)

                # CSVデータに新しいペットの情報を追加
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
                    'image_urls': ', '.join(image_urls)  # 画像URLをカンマ区切りで保存
                }

                # 新しいペットがCSVに存在しない場合は追加
                if pet.id not in data['id'].values:
                    data = pd.concat([data, pd.DataFrame([new_pet_data])], ignore_index=True)
                    write_csv(data)

                # 作成完了後、完了ページにリダイレクト
                return redirect('petapp:pet-create-comp', pet_id=pet.id)

            except ValidationError as e:
                error_messages.append(f"Validation error: {str(e)}")

    return render(request, 'petapp/pet_create.html', {
        'form': pet_form,
        'photo_formset': photo_formset,
        'error_messages': error_messages,
        'csv_data': data.head()  # CSVデータを表示
    })


# ペット作成完了ビュー
def pet_create_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet_images = PetImage.objects.filter(pet=pet)
    return render(request, 'petapp/pet_create_comp.html', {
        'pet': pet,
        'pet_images': pet_images,
    })


def pet_update_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    existing_images = PetImage.objects.filter(pet=pet)

    PetImageFormSet = modelformset_factory(
        PetImage,
        form=PetImageForm,
        extra=5 - existing_images.count(),
        max_num=5,
        can_delete=True,
    )

    updated_fields = []
    old_pet_data = {}

    if request.method == 'POST':
        pet_form = PetUpdateForm(request.POST, instance=pet)
        image_formset = PetImageFormSet(request.POST, request.FILES, queryset=existing_images)

        if pet_form.is_valid() and image_formset.is_valid():
            # 変更前の値を保存
            old_pet_data = {
                'type': pet.type,
                'size': pet.size,
                'color': pet.color,
                'age': pet.age,
                'syu': pet.syu,
                'disease': pet.disease,
                'personality': pet.personality,
                'sex': pet.sex,
            }

            pet_form.save()

            # フィールドの比較と更新内容をリストに追加
            for field, old_value in old_pet_data.items():
                new_value = getattr(pet, field)
                if old_value != new_value:
                    updated_fields.append(f"{field}: {old_value} → {new_value}")

            # 画像の保存・削除
            for form in image_formset:
                if form.cleaned_data.get('DELETE') and form.instance.pk:
                    if default_storage.exists(form.instance.image.path):
                        default_storage.delete(form.instance.image.path)
                    form.instance.delete()
                elif form.cleaned_data.get('image'):
                    pet_image = form.save(commit=False)
                    pet_image.pet = pet
                    pet_image.save()

            # 変更されたフィールドをセッションに保存
            if updated_fields:
                request.session['updated_fields'] = updated_fields

            return redirect('petapp:pet-update-comp', pet_id=pet.id)

    else:
        pet_form = PetUpdateForm(instance=pet)
        image_formset = PetImageFormSet(queryset=existing_images)

    return render(request, 'petapp/pet_update.html', {
        'pet_form': pet_form,
        'image_formset': image_formset,
    })


def pet_update_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # セッションから更新されたフィールドを取得
    updated_fields = request.session.get('updated_fields', [])

    return render(request, 'petapp/pet_update_comp.html', {
        'pet': pet,
        'updated_fields': updated_fields,  # 変更されたフィールドを渡す
    })


# ペット削除ビュー
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


# インデックスビュー
def index(request):
    csv_data = read_csv().head()
    return render(request, 'Survey/index.html', {'csv_data': csv_data})
    return render(request, 'Survey/index.html', {'csv_data': data.head()})
