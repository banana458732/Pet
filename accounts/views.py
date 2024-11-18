from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# from .forms import CustomUserCreationForm



class SignUpView(CreateView):

    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:signup_success')

        
    def form_valid(self, form):
        ctx = {'form': form}

        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'accounts/signup_confirm.html', ctx)

        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'accounts/signup.html', ctx)

        if self.request.POST.get('next', '') == 'create':
            cleaned_data = form.cleaned_data
            at_username = cleaned_data['username']
            at_email = cleaned_data['email']
            at_password = cleaned_data['password']

            user_db = User(
                username=at_username,
                email=at_email,
                password=at_password,
            )
            user_db.save()
            return super().form_valid(form)
            # フォームからデータを取得
            # モデルインスタンスの作成

    

class SignUpSuccessView(TemplateView):

    template_name = "accounts/signup_success.html"

class LoginSuccessView(TemplateView):
    template_name = "accounts/login_success.html"

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # もし、ユーザーオブジェクトが存在するなら。
        if user is not None:
        # ログインする。
            login(request, user)
            return redirect('accounts:login_success')
        # ユーザーがオブジェクトが存在しないなら。
        else:
            return render(request, 'accounts/login.html', {'error': 'そのユーザーは存在しません。'})
        
    return render(request, 'accounts/login.html', {})


class IndexView(TemplateView):
    template_name = 'accounts/index.html'