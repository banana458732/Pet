from django import forms
from .models import Pet, PetImage
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage


class PetCreateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['type', 'size', 'color', 'age', 'kinds', 'disease',
                  'personality', 'sex', 'phone_number']

    def clean_id(self):
        """新規登録時にidが空でも許容し、0以下のidは不正とする"""
        id = self.cleaned_data.get('id')
        if id is not None and id <= 0:
            raise ValidationError("IDは1以上でなければなりません。")
        if not self.instance.pk and not id:  # 新規登録時でidが空
            return None
        return id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id' in self.fields:
            self.fields['id'].initial = value  # 初期値を設定
            print(self.fields)  # フィールド全体を出力して確認


class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image']

    image = forms.ImageField(required=False, label='写真')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RequiredPetImageFormSet(modelformset_factory(PetImage, form=PetImageForm, extra=5)):
    def clean(self):
        super().clean()
        # 少なくとも1つの画像がアップロードされているかチェック
        if not any(form.cleaned_data.get('image') for form in self.forms if form.cleaned_data):
            raise ValidationError("少なくとも1つの画像をアップロードしてください。")

        # 新規登録時に画像が未選択でもエラーを防止
        for form in self.forms:
            if not form.cleaned_data.get('image') and form.instance.pk is None:
                form.cleaned_data['image'] = None  # 空のまま進むための処理

    def save(self, commit=True):
        # 保存処理を行う前に画像を削除する場合に備えた処理
        for form in self.forms:
            # 空の画像が送信されている場合、そのまま進む
            if not form.cleaned_data.get('image') and not form.instance.pk:
                continue

            # 保存のためにファイルを管理
            form.save(commit=commit)
        return super().save(commit=commit)


# 使用するフォームセットを変更
PetImageFormSet = RequiredPetImageFormSet


class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['type', 'size', 'color', 'age', 'kinds', 'disease',
                  'personality', 'sex', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # idは入力可能に保つ（必須ではない）
        self.fields['id'].required = False

        # 更新時に id フィールドを非必須に設定
        if self.instance.pk:
            self.fields['id'].required = False  # id フィールドを非必須にする
            self.fields['id'].widget = forms.HiddenInput()  # idを非表示にする
        else:
            self.fields['id'].required = True  # 新規作成時は必須にする

    TYPE_CHOICES = [
        ('犬', '犬'),
        ('猫', '猫'),
    ]

    SIZE_CHOICES = [
        ('大型', '大型'),
        ('中型', '中型'),
        ('小型', '小型'),
    ]

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # idは非必須でHiddenInputにする
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='種類', disabled=True)
    size = forms.ChoiceField(choices=SIZE_CHOICES, label='サイズ')
    color = forms.CharField(max_length=100, label='毛の色')
    age = forms.IntegerField(min_value=0, max_value=10, label='年齢')
    kinds = forms.CharField(max_length=100, label='品種')
    disease = forms.CharField(max_length=100, label='病歴', required=False)
    personality = forms.CharField(max_length=100, label='性格', required=False)
    sex = forms.CharField(label='性別', required=False, disabled=True)
    phone_number = forms.CharField(max_length=15, label='電話番号', required=False)


class PetImageUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        label='画像を更新する',
        widget=forms.ClearableFileInput(attrs={'initial_text': '', 'clear_checkbox_label': 'クリア'})
    )

    class Meta:
        model = PetImage
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        return image

    def save(self, commit=True):
        old_image = self.instance.image
        new_image = self.cleaned_data.get('image')

        # 新しい画像がアップロードされた場合、古い画像を削除
        if old_image and new_image and old_image != new_image:
            image_path = old_image.path
            if default_storage.exists(image_path):
                # 古い画像ファイルを削除
                default_storage.delete(image_path)

        # 新しい画像を保存
        return super().save(commit=commit)


class PetImageUpdateFormSet(modelformset_factory(PetImage, form=PetImageUpdateForm, extra=0, can_delete=True)):
    def clean(self):
        super().clean()

        # 画像の削除と追加が同時に選ばれていないか確認
        for form in self.forms:
            delete_flag = form.cleaned_data.get('DELETE', False)
            image = form.cleaned_data.get('image', None)

            # 削除フラグが立っているのに、画像が設定されている場合はエラー
            if delete_flag and image:
                form.add_error(None, "画像の削除と追加は同時に行えません。どちらか一方を選んでください。")

        # 少なくとも1つの画像が残っていることを確認
        remaining_images = [
            form.cleaned_data.get('image') or form.instance.image
            for form in self.forms
            if not form.cleaned_data.get('DELETE')
        ]

        if not remaining_images:
            raise ValidationError("少なくとも1つの画像をアップロードしてください。")
