from django import forms
from .models import Pet, PetImage
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError


class PetCreateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['id', 'type', 'size', 'color', 'age', 'syu', 'disease',
                  'personality', 'sex', 'phone_number']


class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image']

    image = forms.ImageField(required=True, label='写真')  # ラベルを「写真」に変更


class RequiredPetImageFormSet(modelformset_factory(PetImage, form=PetImageForm, extra=5)):
    def clean(self):
        super().clean()
        if not any([form.cleaned_data.get('image') for form in self.forms if form.cleaned_data]):
            raise ValidationError("少なくとも1つの画像をアップロードしてください。")


# 使用するフォームセットを変更
PetImageFormSet = RequiredPetImageFormSet


class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['id', 'type', 'size', 'color', 'age', 'syu', 'disease',
                  'personality', 'sex', 'phone_number']

    # IDの重複をチェックするバリデーション
    def clean_id(self):
        id = self.cleaned_data.get('id')
        # 現在のオブジェクトのIDを取得（もし存在する場合）
        current_id = self.instance.id

        if id and current_id and id != current_id:
            # 新しいIDがすでに存在する場合
            if Pet.objects.filter(id=id).exists():
                raise forms.ValidationError("このIDはすでに登録されています。別のIDを入力してください。")

        return id

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
    size = forms.ChoiceField(choices=SIZE_CHOICES, label='サイズ', disabled=True)
    color = forms.CharField(max_length=100, label='毛の色')
    age = forms.IntegerField(min_value=0, max_value=30, label='年齢')
    syu = forms.CharField(max_length=100, label='種別')  # 追加
    disease = forms.CharField(max_length=100, label='病歴', required=False)  # 追加
    personality = forms.CharField(max_length=100, label='性格', required=False)  # 追加
    sex = forms.CharField(label='性別', required=False, disabled=True)
    phone_number = forms.CharField(max_length=15, label='電話番号', required=False)  # 追加
