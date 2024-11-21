import os, csv
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
from django.db import transaction
from django.conf import settings


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
        return pd.DataFrame(columns=['id', 'type', 'size', 'color', 'age', 'kinds', 'disease', 'personality', 'sex'])


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
    # 不要な列（Unnamed: 10）を削除
    data = data.drop(columns=['Unnamed: 10'], errors='ignore')

    data.fillna('なし', inplace=True)  # 欠損値を'なし'に埋める

    if request.method == 'POST':
        pet_form = PetCreateForm(request.POST)
        photo_formset = PetImageFormSet(request.POST, request.FILES)

        if pet_form.is_valid() and photo_formset.is_valid():
            try:
                # トランザクション開始
                with transaction.atomic():
                    pet = pet_form.save()  # ペット情報を保存

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
                            image_urls.append(pet_image.image.url)  # 保存した画像のURLをリストに追加

                    # 画像がアップロードされていない場合の処理
                    if not photo_uploaded:
                        error_messages.append("少なくとも1つの画像をアップロードしてください。")
                        pet.delete()  # ペット作成を取り消し
                        return render(request, 'petapp/pet_create.html', {
                            'form': pet_form,
                            'photo_formset': photo_formset,
                            'error_messages': error_messages,
                            'csv_data': data.head()  # CSVデータを表示
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
                        'kinds': pet.kinds,
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
                # トランザクションがロールバックされると、何もデータベースに保存されません

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
        extra=5 - existing_images.count(),  # 既存画像数に基づいて追加するフォーム数を決定
        max_num=5,  # 最大5枚まで画像をアップロード可能
        can_delete=True,  # 画像の削除を許可
    )

    old_pet_data = {}

    if request.method == 'POST':
        old_pet_data = {
            'type': pet.type,
            'size': pet.size,
            'color': pet.color,
            'age': pet.age,
            'kinds': pet.kinds,
            'disease': pet.disease,
            'personality': pet.personality,
            'sex': pet.sex,
        }

        pet_form = PetUpdateForm(request.POST, instance=pet)
        image_formset = PetImageFormSet(request.POST, request.FILES, queryset=existing_images)

        errors = False
        deleted_images = []
        added_images = []
        error_message = None

        if pet_form.is_valid() and image_formset.is_valid():
            # 削除後の残り画像数を計算（削除された画像数を差し引く）
            remaining_images = existing_images.count() - sum(
                1 for form in image_formset if form.cleaned_data.get('DELETE', False)
            )

            # 新しい画像が追加されている場合、残り画像数にカウント
            if any(form.cleaned_data.get('image') for form in image_formset):
                remaining_images += sum(
                    1 for form in image_formset if form.cleaned_data.get('image') is not None and not form.cleaned_data.get('DELETE', False)
                )

            # バリデーション: 削除後に残る画像数が1枚以上であることを確認
            if remaining_images < 1:
                error_message = "画像は1枚以上登録されている必要があります。"
                for form in image_formset:
                    form.add_error(None, error_message)
                errors = True
                image_formset.is_valid = False
                print(error_message)

            if not errors:
                # トランザクション開始
                with transaction.atomic():
                    pet = pet_form.save()  # ペット情報を更新

                    updated_fields = []
                    for field, old_value in old_pet_data.items():
                        new_value = getattr(pet, field)
                        updated_field = f"{field}: {old_value} → {new_value}" if old_value != new_value else f"{field}: {old_value} （変更なし）"
                        updated_fields.append(updated_field)

                    for form in image_formset:
                        delete_flag = form.cleaned_data.get('DELETE', False)
                        image = form.cleaned_data.get('image', None)

                        if delete_flag:
                            image_instance = form.instance
                            if image_instance.pk and image_instance.image:
                                image_path = image_instance.image.path
                                if default_storage.exists(image_path):
                                    print(f"画像 {image_path} を削除します")
                                    default_storage.delete(image_path)
                                    deleted_images.append(image_path)
                            image_instance.delete()  # 画像インスタンス自体を削除

                        elif image:  # 新規画像を追加
                            if form.cleaned_data.get('id'):  # 既存画像の更新
                                existing_image = PetImage.objects.get(id=form.cleaned_data.get('id').id)
                                if existing_image.image and existing_image.image != image:
                                    image_path = existing_image.image.path
                                    if default_storage.exists(image_path):
                                        print(f"新しい画像が選択されたため、既存画像 {image_path} を削除します")
                                        default_storage.delete(image_path)
                                existing_image.image = image
                                existing_image.save()
                                added_images.append(existing_image.image.url)
                            else:  # 新規画像追加
                                pet_image = form.save(commit=False)
                                pet_image.pet = pet
                                pet_image.save()
                                added_images.append(pet_image.image.url)

                    data = read_csv()  # CSVファイルのデータを読み込み
                    for index, row in data.iterrows():
                        if row['id'] == pet.id:
                            data.at[index, 'type'] = pet.type
                            data.at[index, 'size'] = pet.size
                            data.at[index, 'color'] = pet.color
                            data.at[index, 'age'] = pet.age
                            data.at[index, 'kinds'] = pet.kinds
                            data.at[index, 'disease'] = pet.disease
                            data.at[index, 'personality'] = pet.personality
                            data.at[index, 'sex'] = pet.sex
                            data.at[index, 'image_urls'] = ', '.join(added_images)
                            break

                    write_csv(data)

                    request.session['updated_fields'] = updated_fields
                    request.session['added_images'] = added_images
                    request.session['deleted_images'] = deleted_images
                    request.session.modified = True

                return redirect('petapp:pet-update-comp', pet_id=pet.id)

        else:
            print("フォームにエラーがあります")
            print(f"ペットフォームエラー: {pet_form.errors}")
            print(f"画像フォームセットエラー: {image_formset.errors}")

        return render(request, 'petapp/pet_update.html', {
            'pet_form': pet_form,
            'image_formset': image_formset,
            'error_message': error_message,
        })

    else:  # GETリクエスト
        pet_form = PetUpdateForm(instance=pet)
        image_formset = PetImageFormSet(queryset=existing_images)

        return render(request, 'petapp/pet_update.html', {
            'pet_form': pet_form,
            'image_formset': image_formset,
        })


def pet_update_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # セッションから更新されたフィールドを取得し、取得後に削除
    updated_fields = request.session.pop('updated_fields', [])

    # ラベル変換辞書
    field_labels = {
        'age': '歳',
        'type': '種類',
        'size': 'サイズ',
        'color': '色',
        'kinds': '種別',
        'disease': '病歴',
        'personality': '性格',
        'sex': '性別',
    }

    # updated_fieldsを日本語ラベルに変換
    localized_updated_fields = []
    for field in updated_fields:
        field_name, changes = field.split(": ", 1)
        localized_field_name = field_labels.get(field_name, field_name)  # 日本語ラベルに変換
        localized_updated_fields.append(f"{localized_field_name}: {changes}")

    # 画像のURLを取得
    pet_images = PetImage.objects.filter(pet=pet)

    return render(request, 'petapp/pet_update_comp.html', {
        'pet': pet,
        'updated_fields': localized_updated_fields,  # 日本語ラベルのフィールドを渡す
        'pet_images': pet_images,  # 画像の情報を渡す
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
