from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
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
            return super().form_valid(form)
            # フォームからデータを取得
            # モデルインスタンスの作成
        return render(self.request, 'accounts/signup.html', ctx)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 他の必要なコンテキストデータを渡す
        return context


class SignUpSuccessView(TemplateView):

    template_name = "accounts/signup_success.html"


def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # もし、ユーザーオブジェクトが存在するなら。
        if user is not None:
        # ログインする。
            login(request, user)
            return redirect('accounts:index')
        # ユーザーがオブジェクトが存在しないなら。
        else:
            return render(request, 'accounts/login.html', {'error': 'そのユーザーは存在しません。'})
        
    return render(request, 'accounts/login.html', {})


class IndexView(TemplateView):
    template_name = 'accounts/index.html'


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'

