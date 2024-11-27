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
