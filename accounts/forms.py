from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms 

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(label="住所", max_length=31, required=True)
    phone_number = forms.CharField(label='電話番号', max_length=15, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','address','phone_number')


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
