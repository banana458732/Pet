from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validate_phone_number(value):
    if not re.match(r'^\d{2,4}-\d{2,4}-\d{4}$', value):
        raise ValidationError('有効な電話番号の形式で入力してください（例: 090-1234-5678）。')


def validate_address(value):
    if not re.match(r'^[\w\s\-、。、・〒]+$',value):
        raise ValidationError('有効な住所を入力してください。記号や特殊文字は使用できません。')    


class CustomUserCreationForm(UserCreationForm):

    address = forms.CharField(label="住所", min_length=10, max_length=31, required=True, widget=forms.TextInput(attrs={'placeholder': '例: 長野県長野市長野元善町491番地'}), validators=[validate_address])
    phone_number = forms.CharField(label='電話番号', max_length=15, required=True,widget=forms.TextInput(attrs={'placeholder': '例: 090-0000-0000'}) ,validators=[validate_phone_number])
    username = forms.CharField(label="ユーザーネーム", min_length=3, max_length=16, required=True,widget=forms.TextInput(attrs={'placeholder': '例: pet123'}))
    email = forms.EmailField(label="メールアドレス", min_length=7, max_length=256, required=True,widget=forms.TextInput(attrs={'placeholder': '例: pet@pet.com'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'address', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ラベルからコロンを削除
        for field in self.fields.values():
            field.label_suffix = ''  # コロンを削除


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class ProfileImageForm(forms.ModelForm):
    delete_image = forms.BooleanField(required=False, label='画像を削除', initial=False)

    class Meta:
        model = CustomUser
        fields = ['profile_image']

    # フィールドにカスタムウィジェットを設定
    profile_image = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        label=''
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('delete_image'):  # 画像を削除する場合
            instance.delete_old_image()
            instance.profile_image = 'profile_images/default.jpg'  # デフォルト画像に戻す
        if commit:
            instance.save()
        return instance


class CustomUserUpdateForm(forms.ModelForm):
    """ユーザー情報編集フォーム"""
    address = forms.CharField(
        label="住所",
        min_length=10,
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: 長野県長野市元善町491'}),
        validators=[validate_address]
    )
    phone_number = forms.CharField(
        label="電話番号",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: 090-1234-5678'}),
        validators=[validate_phone_number]
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ラベルのコロンを削除
        for field in self.fields.values():
            field.label_suffix = ""
