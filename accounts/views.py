from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.contrib import messages
from petapp.models import Pet
from karikeiyaku.models import Karikeiyaku
from .forms import ProfileImageForm
from petapp.models import PetImage
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

class SignUpView(CreateView):

    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        ctx = {'form': form}

        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'accounts/signup_confirm.html', ctx)

        # if self.request.POST.get('next', '') == 'back':
        #     return render(self.request, 'accounts/signup.html', ctx)

        # if self.request.POST.get('next', '') == 'create':
        #     return super().form_valid(form)
            # フォームからデータを取得
            # モデルインスタンスの作成
        return render(self.request, 'accounts/signup.html', ctx)
    
class SignUp_ConfirmView(CreateView):
    template_name = "accounts/signup_confirm.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'create':
            return render(self.request, 'accounts/signup_success', ctx)
        return render(self.request, 'accounts/signup_confirm', ctx)
    



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 他の必要なコンテキストデータを渡す
        return context


class SignUpSuccessView(TemplateView):

    template_name = "accounts/signup_success.html"


def LoginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        # もし、ユーザーオブジェクトが存在するなら。
        if user is not None:
        # ログインする。
            login(request, user)
            return redirect('accounts:index')  # トップページのURLパターンにリダイレクト

        # ユーザーがオブジェクトが存在しないなら。
        else:
            return render(request, 'accounts/login.html', {'error': 'そのユーザーは存在しません。'})

    return render(request, 'accounts/login.html', {})

def is_staff(user):
    return user.is_staff


@staff_member_required
def staff_menu(request):
    return HttpResponse('staff')


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/my_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 仮契約中のペット情報を取得
        contract_pets = Karikeiyaku.objects.filter(user=user, status="仮契約中").select_related('pet')

        for contract_pet in contract_pets:
            print(f"契約開始日: {contract_pet.created_at}")
            print(f"契約終了日: {contract_pet.end_date}")
            print(f"契約状態: {contract_pet.status}")

        # 仮契約中のペットの画像を取得
        pet_images = []
        for contract_pet in contract_pets:
            pet = contract_pet.pet

            if pet:  # petが存在するか確認
                # PetImageモデルに関連する画像を取得
                images = PetImage.objects.filter(pet=pet)

                # 画像情報とペット情報をまとめて辞書に格納
                pet_images.append({
                    'pet': pet,
                    'images': images if images.exists() else None,
                    'created_at': contract_pet.created_at,
                    'end_date': contract_pet.end_date,
                    'status': contract_pet.status
                })

        context['pet_images'] = pet_images  # ここで画像情報を追加

        # プロフィール画像フォームをコンテキストに追加
        context['profile_image_form'] = ProfileImageForm(instance=user)

        return context


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


def change_profile_image(request):
    """プロフィール画像と登録情報を変更するビュー"""
    user = request.user

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=user)  # ユーザー情報用フォーム
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=user)  # プロフィール画像用フォーム

        # 両方のフォームが有効であれば保存
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:my_page')  # 保存後にマイページへリダイレクト
    else:
        # 初期値を設定
        user_form = CustomUserUpdateForm(instance=user)
        profile_form = ProfileImageForm(instance=user)

    # コンテキストに両方のフォームを渡す
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/change_profile_image.html', context)


class IndexView(TemplateView):
    template_name = 'accounts/index.html'


class RedirectTemporaryPetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # 仮契約中のペット情報を取得
            contract_pets = Karikeiyaku.objects.filter(user=user, status="仮契約中").select_related('pet')
            print(contract_pets.count())

            if contract_pets.count() == 1:
                # 仮契約中のペットが1匹だけの場合、その詳細ページにリダイレクト
                return redirect('messaging:pet_detail', pet_id=contract_pets.first().pet.id)
            elif contract_pets.count() > 1:
                # 仮契約中のペットが複数匹いる場合、選択画面にリダイレクト
                return redirect('accounts:pet_selection')

        # 仮登録中のペットがない場合は元のページに戻る
        messages.info(request, '仮登録中のペットがありません。')
        previous_page = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_page)

        # return redirect(previous_page, {'no_petmessage': '現在登録中のペットがありません。'})


class PetSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/pet_selection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['contract_pets'] = Karikeiyaku.objects.filter(user=user, status="仮契約中").select_related('pet')
        return context


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'


def index(request):
    # PetImageテーブルから全ての画像データを取得
    pets = Pet.objects.all()
    return render(request, 'accounts/index.html', {'pets': pets})
