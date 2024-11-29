from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
# Create your views here.
from django.views import View
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
from petapp.models import Pet
from karikeiyaku.models import Karikeiyaku


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


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/my_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 仮契約中のペット情報を取得
        contract_pets = Karikeiyaku.objects.filter(user=user, status="仮契約中").select_related('pet')

        # Debugging output
        print(f"User: {user.username}")
        print(f"Contract Pets: {contract_pets}")

        context['contract_pets'] = contract_pets

        return context
    
    def post(self, request, *args, **kwargs):
        # Here we set a session flag before redirecting to cancel
        pet_id = request.POST.get('pet_id')
        if pet_id:
            request.session['from_mypage'] = True
            return redirect('karikeiyaku:cancel', pet_id=pet_id)
        return super().post(request, *args, **kwargs)


def add_contract_pet(request, pet_id):
    user = request.user
    if not user.is_authenticated:
        return redirect('accounts:login')

    pet = get_object_or_404(Pet, id=pet_id)  # ペットを取得

    # デバッグ用ログ
    print(f"User: {user.username}")
    print(f"Adding pet ID: {pet.id} - {pet}")

    # 仮契約を作成
    Karikeiyaku.objects.create(user=user, pet=pet, status="仮契約中")

    # 追加後の確認
    print(f"Contract Pets after addition: {user.karikeiyaku.filter(status='仮契約中')}")

    return redirect('accounts:my_page')


def complete_contract(request):
    user = request.user
    if not user.is_authenticated:  # ユーザーがログインしているか確認
        return redirect('accounts:login')

    # 仮契約を完了に更新
    user.contract_status = '完了'
    user.save()  # ユーザー情報を保存

    return redirect('accounts:my_page')  # マイページへリダイレクト


class IndexView(TemplateView):
    template_name = 'accounts/index.html'


class RedirectTemporaryPetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # 仮契約中のペット情報を取得
            contract_pet = Karikeiyaku.objects.filter(user=user, status="仮契約中").select_related('pet').first()
            
            if contract_pet:
                return redirect('messaging:pet_detail', pet_id=contract_pet.pet.id)


        # 仮登録中のペットがない場合はトップページに戻る
        return render(request, 'accounts/index.html', {'has_temporary_pet': contract_pet})


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'

from django.shortcuts import render
from petapp.models import PetImage

def index(request):
    # PetImageテーブルから全ての画像データを取得
    images = PetImage.objects.all()
    return render(request, 'accounts/index.html', {'images': images})
