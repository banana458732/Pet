from django import forms
from .models import Pet, PetImage
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError


class PetCreateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['id', 'type', 'size', 'color', 'age', 'syu', 'disease',
                  'personality', 'sex', 'phone_number']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 0 or age > 30):
            raise ValidationError('年齢は0から30の範囲で入力してください。')
        return age


class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image']

    image = forms.ImageField(required=False, label='写真')

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise ValidationError("画像が必要です。")  # エラーを発生させる
        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 画像が空の場合、初期値をクリア
        if not self.instance.image:
            self.fields['image'].initial = None


class RequiredPetImageFormSet(modelformset_factory(PetImage, form=PetImageForm, extra=5)):
    def clean(self):
        super().clean()
        # 少なくとも1つの画像がアップロードされているかチェック
        if not any(form.cleaned_data.get('image') for form in self.forms if form.cleaned_data):
            raise ValidationError("少なくとも1つの画像をアップロードしてください。")


# 使用するフォームセットを変更
PetImageFormSet = RequiredPetImageFormSet


class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['id', 'type', 'size', 'color', 'age', 'syu', 'disease',
                  'personality', 'sex', 'phone_number']

    TYPE_CHOICES = [
        ('犬', '犬'),
        ('猫', '猫'),
    ]

    SIZE_CHOICES = [
        ('大型', '大型'),
        ('中型', '中型'),
        ('小型', '小型'),
    ]

    id = forms.IntegerField(widget=forms.HiddenInput())
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='種類', disabled=True)
    size = forms.ChoiceField(choices=SIZE_CHOICES, label='サイズ')  # サイズを編集可能に変更
    color = forms.CharField(max_length=100, label='毛の色')
    age = forms.IntegerField(min_value=0, max_value=30, label='年齢')
    syu = forms.CharField(max_length=100, label='種別')  # 追加
    disease = forms.CharField(max_length=100, label='病歴', required=False)  # 追加
    personality = forms.CharField(max_length=100, label='性格', required=False)  # 追加
    sex = forms.CharField(label='性別', required=False, disabled=True)
    phone_number = forms.CharField(max_length=15, label='電話番号', required=False)  # 追加
