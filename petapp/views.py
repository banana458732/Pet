import os
import uuid
import pandas as pd
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from .models import Pet, PetImage, PhoneNumber
from .forms import PetCreateForm, PetImageFormSet, PetUpdateForm, PetImageForm
from django.forms import modelformset_factory
from django.core.files.storage import default_storage
from django.db import transaction
import requests


# CSVファイルのパスを指定
CSV_FILE_PATH = os.getenv('PETS_CSV_PATH', 'pets_data.csv')

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
    template_name = 'petapp/admin/pet_list.html'
    ordering = ['-id']  # 新しいペットを上に表示
    paginate_by = 12  # 1ページあたり10件のペットを表示


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

    # 不要な列（Unnamed: 10）を削除
    data = data.drop(columns=['Unnamed: 10'], errors='ignore')

    if request.method == 'POST':
        pet_form = PetCreateForm(request.POST)
        photo_formset = PetImageFormSet(request.POST, request.FILES)

        if pet_form.is_valid() and photo_formset.is_valid():
            try:
                # トランザクション開始
                with transaction.atomic():
                    pet = pet_form.save()  # ペット情報を保存
                    pet_id = pet.id

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
                    phone_number = str(request.POST.get('phone_number', '')).strip()
                    if phone_number:
                        PhoneNumber.objects.create(pet=pet, number=phone_number)

                    # ペットのIDを確認した後にCSVにデータを追加
                    new_pet_data = {
                        'id': str(pet_id),  # IDを文字列として扱う
                        'type': pet.type,
                        'size': pet.size,
                        'color': pet.color,
                        'age': pet.age,
                        'kinds': pet.kinds,
                        'disease': pet.disease,
                        'personality': pet.personality,
                        'sex': pet.sex,
                        'post_code': str(pet.post_code).strip(),  # 郵便番号を文字列として扱う
                        'address': pet.address,
                        'phone_number': phone_number,  # 文字列として保存
                        'location': pet.location,
                        'image_urls': ', '.join(image_urls)  # 画像URLをカンマ区切りで保存
                    }

                    # 新しいペットがCSVに存在しない場合は追加
                    if str(pet_id) not in data['id'].astype(str).values:
                        data = pd.concat([data, pd.DataFrame([new_pet_data])], ignore_index=True)
                        write_csv(data)

                    return redirect('petapp:pet-create-comp', pet_id=pet.id)
            except ValidationError as e:
                # ValidationErrorが発生した場合、エラーメッセージをキャッチ
                error_messages.append(f"Validation error: {str(e)}")
                # トランザクションがロールバックされると、何もデータベースに保存されません
                return render(request, 'petapp/pet_create.html', {
                    'form': pet_form,
                    'photo_formset': photo_formset,
                    'csv_data': data.head(),  # CSVデータを表示
                })

    # ペット作成フォームと画像フォームセットを含むビューをレンダリング
    return render(request, 'petapp/pet_create.html', {
        'form': pet_form,
        'photo_formset': photo_formset,
        'error_messages': error_messages,
        'csv_data': data.head(),  # CSVデータを表示
    })


# ペット作成完了ビュー
def pet_create_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet_images = PetImage.objects.filter(pet=pet)
    formatted_phone_number = pet.formatted_phone_number()

    return render(request, 'petapp/pet_create_comp.html', {
        'pet': pet,
        'pet_images': pet_images,
        'formatted_phone_number': formatted_phone_number,  # フォーマット済み電話番号
    })


def pet_update_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    existing_images = PetImage.objects.filter(pet=pet)

    # フォームセットの作成: 画像追加フォームの数を計算
    PetImageFormSet = modelformset_factory(
        PetImage,
        form=PetImageForm,
        extra=5 - existing_images.count(),  # 既存画像数に基づいて追加フォーム数を決定
        max_num=5,  # 最大5枚まで画像をアップロード可能
        can_delete=True,  # 画像の削除を許可
    )

    old_pet_data = {}  # 変更前のペットデータを保存

    if request.method == 'POST':
        # 変更前のペットデータを保存
        old_pet_data = {
            'type': pet.type,
            'size': pet.size,
            'color': pet.color,
            'age': pet.age,
            'kinds': pet.kinds,
            'disease': pet.disease,
            'personality': pet.personality,
            'sex': pet.sex,
            'post_code': pet.post_code,
            'address': pet.address,
            'phone_number': pet.phone_number,
            'location': pet.location,
        }

        # 変更前のペット住所を保存
        request.session['old_pet_address'] = pet.address


        # フォームの初期化
        pet_form = PetUpdateForm(request.POST, instance=pet)
        image_formset = PetImageFormSet(request.POST, request.FILES, queryset=existing_images)

        errors = False
        updated_images = []  # 変更された画像URLを格納するリスト
        deleted_images = []  # 削除された画像URLを格納するリスト
        added_images = []  # 新規追加された画像URLを格納するリスト
        error_message = None

        logger = logging.getLogger(__name__)

        if pet_form.is_valid() and image_formset.is_valid():
            # 削除後に残る画像数を計算
            remaining_images = existing_images.count() - sum(
                1 for form in image_formset if form.cleaned_data.get('DELETE', False)
            )

            # 新規画像が追加されている場合はカウントを増やす
            remaining_images += sum(
                1 for form in image_formset if form.cleaned_data.get('image') and not form.cleaned_data.get('DELETE', False)
            )

            # バリデーション: 削除後に残る画像数が1枚以上であることを確認
            if remaining_images < 1:
                error_message = "画像は1枚以上登録されている必要があります。"
                for form in image_formset:
                    form.add_error(None, error_message)
                errors = True
                image_formset.is_valid = False

            if not errors:
                # トランザクション開始
                with transaction.atomic():
                    pet = pet_form.save()  # ペット情報を更新

                    # 新しいペットの住所をセッションに保存。
                    request.session['new_pet_address'] = pet.address

                    updated_fields = []
                    for field, old_value in old_pet_data.items():
                        # Noneを空文字列に変換して比較
                        old_value = old_value if old_value is not None else ""
                        new_value = getattr(pet, field) if getattr(pet, field) is not None else ""

                        if old_value != new_value:
                            updated_field = f"{field}: {new_value}"
                            updated_fields.append(updated_field)

                    # 画像削除処理
                    for form in image_formset:
                        delete_flag = form.cleaned_data.get('DELETE', False)
                        image = form.cleaned_data.get('image', None)

                        if delete_flag:
                            # 画像の削除処理
                            image_instance = form.instance
                            if image_instance.pk:  # IDが存在する場合のみ削除
                                if image_instance.image:
                                    image_path = image_instance.image.path
                                    if default_storage.exists(image_path):
                                        default_storage.delete(image_path)
                                    deleted_images.append(image_instance.image.url)  # 削除された画像URLを追加
                                image_instance.delete()  # 画像インスタンスを削除
                        elif image:
                            # 新規画像を追加または既存画像を更新
                            if form.cleaned_data.get('id'):
                                existing_image = PetImage.objects.get(id=form.cleaned_data.get('id').id)
                                if existing_image.image and existing_image.image != image:
                                    # 画像が変更されている場合、更新された画像として処理
                                    updated_images.append(existing_image.image.url)  # 更新された画像をリストに追加
                                    image_path = existing_image.image.path
                                    if default_storage.exists(image_path):
                                        default_storage.delete(image_path)
                                existing_image.image = image
                                existing_image.save()
                            else:
                                pet_image = form.save(commit=False)
                                pet_image.pet = pet
                                pet_image.save()
                                added_images.append(pet_image.image.url)  # 新規追加された画像をリストに追加

                    try:
                        data = read_csv()  # CSVファイルのデータを読み込む
                        for index, row in data.iterrows():
                            if row['id'] == pet.id:
                                # 新しい画像URLリストを作成
                                existing_image_urls = [
                                    image.image.url for image in existing_images
                                    if image.image and image.pk not in [img.instance.pk for img in image_formset if img.cleaned_data.get('DELETE', False)]
                                ]
                                final_image_urls = list(dict.fromkeys(existing_image_urls + added_images))  # 重複排除

                                # 行データを更新
                                data.at[index, 'type'] = pet.type
                                data.at[index, 'size'] = pet.size
                                data.at[index, 'color'] = pet.color
                                data.at[index, 'age'] = pet.age
                                data.at[index, 'kinds'] = pet.kinds
                                data.at[index, 'disease'] = str(pet.disease) if pet.disease else ''
                                data.at[index, 'personality'] = pet.personality
                                data.at[index, 'sex'] = pet.sex
                                data.at[index, 'post_code'] = str(int(pet.post_code)) if pet.post_code.isdigit() else pet.post_code
                                data.at[index, 'address'] = pet.address
                                data.at[index, 'phone_number'] = str(int(pet.phone_number)) if pet.phone_number.isdigit() else pet.phone_number
                                data.at[index, 'location'] = pet.location
                                data.at[index, 'image_urls'] = ', '.join(final_image_urls)

                                break

                        write_csv(data)  # CSVに書き込み
                    except Exception as e:
                        logger.error(f"CSVの書き込みに失敗しました: {e}")
                        raise e

                    # セッションに変更内容を保存
                    request.session['updated_fields'] = updated_fields
                    request.session['added_images'] = added_images
                    request.session['updated_images'] = updated_images  # 更新された画像をセッションに保存
                    request.session['deleted_images'] = deleted_images
                    request.session.modified = True

                return redirect('petapp:pet-update-comp', pet_id=pet.id)

        else:
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


# 住所から緯度経度を求めるメソッド
def get_lat_lng(address, api_key):

    api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(api_url)
    data = response.json()
    print(api_url)

    if data['status'] == 'OK':
        print(data)
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        raise Exception(f"Error fetching coordinates for address: {address}")


def pet_update_comp_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # セッションから更新されたフィールドを取得し、取得後に削除
    updated_fields = request.session.pop('updated_fields', [])
    added_images = request.session.pop('added_images', [])
    updated_images = request.session.pop('updated_images', [])
    deleted_images = request.session.pop('deleted_images', [])
    session_address = request.session.pop('old_pet_address', None)
    new_session_address = request.session.pop('new_pet_address', None)
    # ラベル変換辞書
    field_labels = {
        'age': '歳',
        'type': '種類',
        'size': 'サイズ',
        'color': '色',
        'kinds': '品種',
        'disease': '病歴',
        'personality': '性格',
        'sex': '性別',
        'post_code': '郵便番号',
        'address': '住所',
        'phone_number': '電話番号',
        'location': '保護施設',
    }

    # updated_fieldsを日本語ラベルに変換
    localized_updated_fields = []
    for field in updated_fields:
        field_name, changes = field.split(": ", 1)
        localized_field_name = field_labels.get(field_name, field_name)  # 日本語ラベルに変換
        localized_updated_fields.append(f"{localized_field_name}: {changes}")

    # 住所が変更されたら緯度経度も変更する処理。
    # session_address = request.session.get['old_pet_address']
    if  session_address != new_session_address:
        print("hoge")
        try:
            adr = new_session_address
            apikey = "AIzaSyDPU-IPGOS4Fyj47WdcVU6pwAPeljw-lHo&q"
            # api_key = "AIzaSyDPU-IPGOS4Fyj47WdcVU6pwAPeljw-lHo&q"
            lat, lng = get_lat_lng(adr, apikey)
            pet.latitude = lat
            pet.longitude = lng
            print(lat)
            pet.save()
        except Exception as e:
            print(e)

    # 完了画面でのメッセージ表示の準備
    messages = []

    # 画像が変更された場合
    if added_images or updated_images or deleted_images:
        messages.append("画像が変更されました。")

    return render(request, 'petapp/pet_update_comp.html', {
        'pet': pet,
        'updated_fields': localized_updated_fields,  # 日本語ラベルのフィールドを渡す
        'messages': messages,  # メッセージリストを渡す
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
