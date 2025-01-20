from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validate_phone_number(value):
    if not re.match(r'^\d{2,4}\d{2,4}\d{4}$', value):
        raise ValidationError('電話番号は半角数字のみで、10～15桁にしてください。(例: 09012345678)')


def validate_address(value):
    if not re.match(r'^[\w\s\-、。、・〒]+$', value):
        raise ValidationError('有効な住所を入力してください。記号や特殊文字は使用できません。')    


def validate_username(value):
    if not re.match(r'^[\w]+$', value):
        raise ValidationError('英数字とアルファベット、_のみ用いて入力してください。')


def validate_post_code(value):
    if not re.match(r'^\d{7}', value):
        raise ValidationError('郵便番号は半角数字のみで入力してください。')
    

def validate_street_address(value):
    if not re.match(r'^\d{1,6}', value):
        raise ValidationError('番地は半角数字とハイフンのみで入力してください。')
    

def validate_email(value):
    if not re.match(r'.*', value):
        raise ValidationError('メールアドレスエラー')

class CustomUserCreationForm(UserCreationForm):

    
    phone_number = forms.CharField(label='電話番号', max_length=15, required=True,widget=forms.TextInput(attrs={'placeholder': '例: 00012345678'}), validators=[validate_phone_number])
    username = forms.CharField(label="ユーザーネーム", min_length=3, max_length=16, required=True,widget=forms.TextInput(attrs={'placeholder': '例: pet123'}), validators=[validate_username])
    email = forms.EmailField(label="メールアドレス", min_length=7, max_length=256, required=True,widget=forms.TextInput(attrs={'placeholder': '例: pet@pet.com'}),validators=[validate_email])
    post_code = forms.CharField(label="郵便番号", min_length=7,max_length=7, required=True,widget=forms.TextInput(attrs={'class': 'p-postal-code', 'placeholder': '例:8900053'}), validators=[validate_post_code])
    street_address = forms.CharField(label="番地",max_length=6, required=True,widget=forms.TextInput(attrs={'class': 'p-extended-address', 'placeholder': '例:10'}),validators=[validate_street_address])
    address1 = forms.CharField(label="都道府県 市区町村", max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'p-region p-locality p-street-address p-extended-address', 'placeholder': '例: 長野県長野市長野元善町'}))
    address2 = forms.CharField(label="建物名", max_length=20, required=False, widget=forms.TextInput(attrs={'class': '','placeholder': '記入例：キャンセビル'}) )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'address1', 'phone_number','post_code','street_address')

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
    address1 = forms.CharField(
        label="都道府県 市区町村",
        min_length=10,
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: 長野県長野市元善町'}),
        validators=[validate_address]  # 必要に応じてカスタムバリデータを追加
    )
    street_address = forms.CharField(
        label="番地",
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: 10番地'}),
        validators=[validate_street_address]  # 必要に応じてバリデータを追加
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
        fields = ['username', 'email', 'address1', 'street_address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ラベルのコロンを削除
        for field in self.fields.values():
            field.label_suffix = ''
