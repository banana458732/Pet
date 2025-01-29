from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.urls import reverse_lazy
from django.views import View
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CustomUser
from django.contrib import messages
from petapp.models import Pet
from karikeiyaku.models import Karikeiyaku
from .forms import ProfileImageForm
from petapp.models import PetImage
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="test")

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


class SignUp_ConfirmView(CreateView):
    template_name = "accounts/signup_confirm.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)

        elif self.request.POST.get('next', '') == 'back':
            return render(self.request, 'accounts/signup.html', ctx)

        return render(self.request, 'accounts/signup_confirm.html', ctx)

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
            next_url = request.GET.get('next', 'accounts:index')
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
                next_url = 'accounts:index'
            return redirect(next_url)  # トップページのURLパターンにリダイレクト

        # ユーザーがオブジェクトが存在しないなら。
        else:
            return render(request, 'accounts/login.html', {'error': 'そのユーザーは存在しません。'})

    return render(request, 'accounts/login.html', {})


def is_staff(user):
    return user.is_staff

# 管理者専用ページ
@staff_member_required(login_url='/accounts/')
@login_required
def Staff_Menu(request):
    return render(request, 'accounts/staff_menu.html')


class Staff_menu(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/staff_pet.html'

    # スタッフ権限をチェックする
    def test_func(self):
        return self.request.user.is_staff

    # 権限がない場合のリダイレクト先を指定
    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('/accounts/login/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 仮契約中のペット情報を取得
        contract_pets_draft = Karikeiyaku.objects.filter(status="仮契約中").select_related('pet')

        # 契約済みのペット情報を取得
        contract_pets_completed = Karikeiyaku.objects.filter(status="契約済み").select_related('pet')

        # 仮契約中のペットの画像を取得
        pet_images_draft = []
        for contract_pet in contract_pets_draft:
            pet = contract_pet.pet
            if pet:  # petが存在するか確認
                images = PetImage.objects.filter(pet=pet)
                pet_images_draft.append({
                    'pet': pet,
                    'images': images if images.exists() else None,
                    'created_at': contract_pet.created_at,
                    'end_date': contract_pet.end_date,
                    'status': contract_pet.status
                })

        # 契約済みのペットの画像を取得
        pet_images_completed = []
        for contract_pet in contract_pets_completed:
            pet = contract_pet.pet
            if pet:  # petが存在するか確認
                images = PetImage.objects.filter(pet=pet)
                pet_images_completed.append({
                    'pet': pet,
                    'images': images if images.exists() else None,
                    'created_at': contract_pet.created_at,
                    'end_date': contract_pet.end_date,
                    'status': contract_pet.status
                })

        # 仮契約中と契約済みのペットを分けてcontextに渡す
        context['pet_images_draft'] = pet_images_draft
        context['pet_images_completed'] = pet_images_completed

        return context


class CompletedPetsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/completed_pets.html'

    # 管理者権限をチェック
    def test_func(self):
        return self.request.user.is_superuser

    # 権限がない場合のリダイレクト先
    def handle_no_permission(self):
        return redirect('/accounts/login/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 契約済みのペット情報を取得
        contract_pets_completed = Karikeiyaku.objects.filter(status="契約済み").select_related('pet')

        # 契約済みのペットの画像を取得
        pet_images_completed = []
        for contract_pet in contract_pets_completed:
            pet = contract_pet.pet
            if pet:  # petが存在するか確認
                images = PetImage.objects.filter(pet=pet)
                pet_images_completed.append({
                    'pet': pet,
                    'images': images if images.exists() else None,
                    'created_at': contract_pet.created_at,
                    'end_date': contract_pet.end_date,
                    'status': contract_pet.status
                })

        context['pet_images_completed'] = pet_images_completed
        return context


def get_lat_lon_from_address(address):
    # Nominatimインスタンスの作成
    geolocator = Nominatim(user_agent="myGeocoder")  # user_agentに任意の名前を設定
    try:
        # ジオコーディングで住所を検索
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None  # 見つからなかった場合
    except Exception as e:
        print(f"エラー: {e}")
        return None, None


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/my_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 仮契約中のペット情報を取得
        contract_pets = Karikeiyaku.objects.filter(user=user, status="仮契約中").select_related('pet')
        
        # 契約済みのペット情報を取得
        completed_pets = Karikeiyaku.objects.filter(user=user, status='契約済み').select_related('pet')

        # 仮契約中のペットの画像を取得
        pet_images = []
        for contract_pet in contract_pets:
            pet = contract_pet.pet
            if pet:  # petが存在するか確認
                images = PetImage.objects.filter(pet=pet)
                pet_images.append({
                    'pet': pet,
                    'images': images if images.exists() else None,
                    'created_at': contract_pet.created_at,
                    'end_date': contract_pet.end_date,
                    'status': contract_pet.status
                })
            # ペットに緯度経度の情報がなかった場合。
            if not pet.latitude and not pet.longitude:
                print("hoge")
                try:
                    adr = pet.address
                    apikey = "AIzaSyDPU-IPGOS4Fyj47WdcVU6pwAPeljw-lHo&q"
                    # api_key = "AIzaSyDPU-IPGOS4Fyj47WdcVU6pwAPeljw-lHo&q"
                    lat, lng = get_lat_lng(adr, apikey)
                    pet.latitude = lat
                    pet.longitude = lng
                    print(lat)
                    print(lng)
                    print(contract_pet)
                    print(contract_pets)
                    pet.save()
                
                    print(f"住所: {adr}")
                    print(f"緯度: {lat}, 経度: {lng}")
                except Exception as e:
                    print(e)
            
        # 契約済みのペットの画像を取得
        completed_pet_images = []
        for completed_pet in completed_pets:
            pet = completed_pet.pet
            if pet:  # petが存在するか確認
                images = PetImage.objects.filter(pet=pet)
                completed_pet_images.append({
                    'pet': pet,
                    'images': images if images.exists() else None,
                    'created_at': completed_pet.created_at,
                    'end_date': completed_pet.end_date,
                    'status': completed_pet.status
                })

        # コンテキストにデータを追加
        context['pet_images'] = pet_images  # 仮契約中のペット
        context['completed_pet_images'] = completed_pet_images  # 契約済みのペット

        # プロフィール画像フォームをコンテキストに追加
        context['profile_image_form'] = ProfileImageForm(instance=user)

        return context

# 住所から緯度経度を求めるメソッド


def get_lat_lng(address, api_key):

    api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(api_url)
    data = response.json()
    print(api_url)

    if data['status'] == 'OK':
        print(data)
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        raise Exception(f"Error fetching coordinates for address: {address}")



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
    # 仮契約中および契約済みのペットIDを取得
    excluded_pet_ids = Karikeiyaku.objects.filter(status__in=['仮契約中', '仮契約済', '契約済み']).values_list('pet_id', flat=True)

    # 除外されたペットを除いた一覧を取得
    pets = Pet.objects.exclude(id__in=excluded_pet_ids)
    
    # デバッグ用のログ出力
    print(f"Excluded Pet IDs: {list(excluded_pet_ids)}")
    print(f"Remaining Pets: {pets}")

    return render(request, 'accounts/index.html', {'pets': pets})
