from django import forms
from .models import Pet, PetImage
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage


class PetCreateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['type', 'size', 'color', 'age', 'kinds', 'disease',
                  'personality', 'sex', 'phone_number', 'post_code', 'address', 'location']

        # フィールドごとのエラーメッセージを設定
        error_messages = {
            'phone_number': {
                'invalid': '電話番号は10桁または11桁の数字でなければなりません。',
            },
            'post_code': {
                'invalid': '郵便番号は7桁の数字でなければなりません。',
            },
        }

    def clean_post_code(self):
        post_code = self.cleaned_data['post_code']
        # 郵便番号のバリデーション
        if not post_code.isdigit() or len(post_code) != 7:
            raise ValidationError('郵便番号は7桁の数字でなければなりません。')
        return post_code

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # 電話番号のバリデーション
        if not phone_number.isdigit() or len(phone_number) not in [10, 11]:
            raise ValidationError('電話番号は10桁または11桁の数字でなければなりません。')
        return phone_number

    def clean_age(self):
        age = self.cleaned_data['age']
        # 年齢が整数かどうかの確認
        if age is not None and (age < 0 or age > 10):
            raise ValidationError('年齢は0から10歳の間でなければなりません。')
        return age

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kinds'].widget.attrs['placeholder'] = '例: 柴犬, スコティッシュフォールド'
        self.fields['color'].widget.attrs['placeholder'] = '例: 白, 白黒'
        self.fields['age'].widget.attrs['placeholder'] = '例: 2'
        self.fields['personality'].widget.attrs['placeholder'] = '例: おとなしい, 活発'
        self.fields['disease'].widget.attrs['placeholder'] = '病気がある場合は入力してください'
        self.fields['post_code'].widget.attrs['placeholder'] = '例: 1234567（ハイフンなし）'
        self.fields['address'].widget.attrs['placeholder'] = '例: 東京都渋谷区神南1-1-1'
        self.fields['phone_number'].widget.attrs['placeholder'] = '例: 09012345678（ハイフンなし）'
        self.fields['location'].widget.attrs['placeholder'] = '例: アニマルハウス'
        # print(self.fields)  # フィールドを確認したい場合に使用


class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image']

    image = forms.ImageField(required=False, label='')

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
                  'personality', 'sex', 'phone_number', 'post_code', 'address', 'location']

        # フィールドごとのエラーメッセージを設定
        error_messages = {
            'phone_number': {
                'invalid': '電話番号は10桁または11桁の数字でなければなりません。',
            },
            'post_code': {
                'invalid': '郵便番号は7桁の数字でなければなりません。',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kinds'].widget.attrs['placeholder'] = '例: 柴犬, スコティッシュフォールド'
        self.fields['color'].widget.attrs['placeholder'] = '例: 白, 白黒'
        self.fields['age'].widget.attrs['placeholder'] = '例: 2'
        self.fields['personality'].widget.attrs['placeholder'] = '例: おとなしい, 活発'
        self.fields['disease'].widget.attrs['placeholder'] = '病気がある場合は入力してください'
        self.fields['post_code'].widget.attrs['placeholder'] = '例: 1234567（ハイフンなし）'
        self.fields['address'].widget.attrs['placeholder'] = '例: 東京都渋谷区神南1-1-1'
        self.fields['phone_number'].widget.attrs['placeholder'] = '例: 09012345678（ハイフンなし）'
        self.fields['location'].widget.attrs['placeholder'] = '例: アニマルハウス'

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
    color = forms.CharField(max_length=100, label='色', required=True)
    age = forms.IntegerField(min_value=0, max_value=10, label='年齢', required=True)
    kinds = forms.CharField(max_length=100, label='品種', required=True)
    disease = forms.CharField(max_length=100, label='病歴', required=False)
    personality = forms.CharField(max_length=100, label='性格', required=True)
    sex = forms.CharField(label='性別', required=False, disabled=True)
    phone_number = forms.CharField(max_length=11, label='電話番号', required=True)
    post_code = forms.CharField(max_length=7, label='郵便番号', required=True)  # 郵便番号を入力
    address = forms.CharField(max_length=255, label='住所', required=True)  # 住所を入力
    location = forms.CharField(max_length=255, label='保護施設', required=True)  # 保護施設を入力

    # clean_phone_number メソッドを追加
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        # 小数点が含まれていた場合は削除
        phone_number = phone_number.replace('.', '').replace('-', '')
        if not phone_number.isdigit() or len(phone_number) not in [10, 11]:
            raise forms.ValidationError('電話番号は10桁または11桁の数字でなければなりません。')
        return phone_number

    # clean_post_code メソッドを追加
    def clean_post_code(self):
        post_code = self.cleaned_data.get('post_code', '')
        # 小数点が含まれていた場合は削除
        post_code = post_code.replace('.', '')
        if not post_code.isdigit() or len(post_code) != 7:
            raise forms.ValidationError('郵便番号は7桁の数字でなければなりません。')
        return post_code


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

        self.deleted_images = []
        self.updated_images = []

        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                self.deleted_images.append(form.instance)  # 削除された画像
            elif form.cleaned_data.get('image') and form.instance.image != form.cleaned_data['image']:
                self.updated_images.append({'url': form.cleaned_data['image'].url})  # 更新された画像のURLを格納

        # 少なくとも1つの画像が残っていることを確認
        remaining_images = [
            form.cleaned_data.get('image') or form.instance.image
            for form in self.forms
            if not form.cleaned_data.get('DELETE')
        ]

        if not remaining_images:
            raise ValidationError("少なくとも1つの画像をアップロードしてください。")
