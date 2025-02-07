from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
import re
from django.core.validators import EmailValidator


# バリデータ関数の整理
def validate_phone_number(value):
    if not re.match(r'^\d{2,4}\d{2,4}\d{4}$', value):
        raise ValidationError('電話番号は半角数字のみで、10～15桁にしてください。(例: 09012345678)')


def validate_address(value):
    if not re.match(r'^[ぁ-んァ-ン一-龥0-9a-zA-Z\s\-、。、・〒]+$', value):
        raise ValidationError('有効な住所を入力してください。')


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


# ユーザー作成フォーム
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        label='電話番号',
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: 00012345678'}),
        validators=[validate_phone_number]
    )
    username = forms.CharField(
        label="ユーザーネーム",
        min_length=3,
        max_length=16,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: pet123'}),
        validators=[validate_username]
    )
    email = forms.EmailField(
        label="メールアドレス",
        min_length=7,
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: pet@pet.com'}),
        validators=[EmailValidator(message='有効なメールアドレスを入力してください。')]
    )
    post_code = forms.CharField(
        label="郵便番号",
        min_length=7,
        max_length=7,
        required=True,
        widget=forms.TextInput(attrs={'class': 'p-postal-code', 'placeholder': '例:8900053'}),
        validators=[validate_post_code]
    )
    street_address = forms.CharField(
        label="番地",
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'class': 'p-extended-address', 'placeholder': '例:10'}),
        validators=[validate_street_address]
    )
    address1 = forms.CharField(
        label="都道府県 市区町村",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'p-region p-locality p-street-address p-extended-address', 'placeholder': '例: 長野県長野市長野元善町'})
    )
    address2 = forms.CharField(
        label="建物名",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': '例：キャンセビル'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'address1', 'phone_number', 'post_code', 'street_address', 'address2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''  # ラベルからコロンを削除


# ログインフォーム
class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser


# プロフィール画像フォーム
class ProfileImageForm(forms.ModelForm):
    delete_image = forms.BooleanField(required=False, label='画像を削除', initial=False)

    class Meta:
        model = CustomUser
        fields = ['profile_image']

    profile_image = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        label=''
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('delete_image'):
            instance.delete_old_image()
            instance.profile_image = 'profile_images/default.jpg'
        if commit:
            instance.save()
        return instance


class CustomUserUpdateForm(forms.ModelForm):
    # ユーザー名
    username = forms.CharField(
        label="ユーザー名",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'ユーザー名（英字と数字のみ）',
            'class': 'form-control'
        }),
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9]*$', message='ユーザー名は英字と数字のみで入力してください。')]
    )

    # メールアドレス
    email = forms.EmailField(
        label="メールアドレス",
        min_length=7,
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例: pet@pet.com'}),
    )

    # 郵便番号
    post_code = forms.CharField(
        label="郵便番号",
        max_length=7,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '例: 1234567（ハイフンなし）',
            'class': 'p-postal-code form-control'
        }),
        validators=[validate_post_code]
    )

    # 都道府県 市区町村（例: 長野県長野市）
    address1 = forms.CharField(
        label="都道府県 市区町村",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'p-region p-locality p-street-address p-extended-address form-control',
            'placeholder': '例: 長野県長野市長野元善町'
        }),
        validators=[validate_address]
    )

    # 番地（例: 10番地）
    street_address = forms.CharField(
        label="番地",
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '例: 10番地',
            'class': 'form-control'
        }),
        validators=[validate_street_address]
    )

    # 建物名（任意）
    address2 = forms.CharField(
        label="建物名",
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '例: キャンセビル',
            'class': 'form-control'
        })
    )

    # 電話番号
    phone_number = forms.CharField(
        label="電話番号",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '例: 09012345678（ハイフンなし）',
            'class': 'form-control'
        }),
        validators=[RegexValidator(r'^[0-9]{10,11}$', '電話番号は半角数字のみで、10,11桁までにしてください。')],
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'post_code', 'address1', 'street_address', 'phone_number', 'address2']

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
        for field in self.fields.values():
            field.label_suffix = ''  # ラベルからコロンを削除
