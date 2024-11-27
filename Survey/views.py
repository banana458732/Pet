import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import SimplePetSurveyForm
from .models import SurveyResult
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from petapp.models import Pet


def pet_survey(request):
    form = SimplePetSurveyForm(request.POST or None)

    # CSVファイルの読み込み
    try:
        pets_data = pd.read_csv('pets_data.csv', encoding='utf-8')  # pets_data.csvを読み込む
        pets_data = pets_data.fillna('')  # 欠損値を空文字で埋める
    except Exception as e:
        return HttpResponse(f"CSVファイルの読み込みに失敗しました: {e}")

    if request.method == 'POST' and form.is_valid():
        # フォームから取得するフィールド
        pet_type = form.cleaned_data.get('pet_type')
        size = form.cleaned_data.get('size')
        color = form.cleaned_data.get('color')
        kinds = form.cleaned_data.get('kinds')
        disease = form.cleaned_data.get('disease')
        personality = form.cleaned_data.get('pet_personality')
        sex = form.cleaned_data.get('sex')
        age_range = form.cleaned_data.get('age_range')

        print("フォームから取得したデータ:", pet_type, size, color, kinds, disease, personality, sex, age_range)

        # **ここでフィルタリング処理を追加**
        if pet_type:
            pets_data = pets_data[pets_data['type'] == pet_type]

        # スコア方式で一致項目を計算
        pets_data['score'] = 0  # 初期スコアを0に設定

        # 各フィールドについて一致項目に応じてスコアを加算
        if size:
            pets_data['score'] += (pets_data['size'] == size).astype(int)
        if color:
            pets_data['score'] += (pets_data['color'] == color).astype(int)
        if kinds:
            pets_data['score'] += (pets_data['kinds'] == kinds).astype(int)
        if disease:
            pets_data['score'] += (pets_data['disease'] == disease).astype(int)
        if personality:
            pets_data['score'] += (pets_data['personality'] == personality).astype(int)
        # 性別でフィルタリング
        if sex:
            pets_data = pets_data[pets_data['sex'] == sex]
            pets_data['score'] += 1  # 性別が一致した場合スコア加算

        # 年齢範囲のフィルタリング（年齢条件だけ追加）
        if age_range:
            selected_age_ranges = age_range.split(',')  # カンマで分割して選ばれた範囲をリストに

            # 年齢範囲内のペットを抽出
            age_filtered_pets = pd.DataFrame()  # 空のデータフレームを初期化
            if '0-3' in selected_age_ranges:
                age_filtered_pets = pd.concat([age_filtered_pets, pets_data[pets_data['age'] <= 3]])
            if '4-7' in selected_age_ranges:
                age_filtered_pets = pd.concat([age_filtered_pets, pets_data[(pets_data['age'] >= 4) & (pets_data['age'] <= 7)]])
            if '8-10' in selected_age_ranges:
                age_filtered_pets = pd.concat([age_filtered_pets, pets_data[(pets_data['age'] >= 8) & (pets_data['age'] <= 10)]])

            # 年齢範囲内のペットを若い順に並べる
            age_filtered_pets = age_filtered_pets.sort_values(by='age', ascending=True)

            # 年齢範囲内のペットと年齢範囲外のペットを分ける
            pets_data_outside_range = pets_data[~pets_data.index.isin(age_filtered_pets.index)]

            # まず年齢範囲内のペットを若い順に表示し、その後に年齢範囲外のペットをそのままの順番で表示
            final_sorted_pets = pd.concat([age_filtered_pets, pets_data_outside_range])

        else:
            # 年齢範囲が選択されていない場合は元のデータを使用
            final_sorted_pets = pets_data

        print("スコア計算後のペットデータ:", pets_data[['score']])  # デバッグ用

        # 年齢範囲が選ばれている場合、その範囲内で若い順に並べる
        sorted_pets = final_sorted_pets.to_dict('records')

        # 画像URLの処理
        pet_with_images = []
        for pet in sorted_pets:
            image_urls = pet.get('image_urls', '')
            first_image = image_urls.split(',')[0] if image_urls else None
            pet_with_images.append((pet, first_image))

        print("マッチング結果:", pet_with_images)

        # SurveyResultを保存
        survey_result = SurveyResult.objects.create(
            pet_type=pet_type or '',
            size=size or '',
            color=color or '',
            kinds=kinds or '',
            disease=disease or '',
            pet_personality=personality or '',
            sex=sex or '',
            age_range=", ".join(age_range) if age_range else ''
        )
        print("SurveyResultが作成されました:", survey_result)

        return render(request, 'survey/results.html', {
            'survey_result': survey_result,
            'pets': pet_with_images,
            'MEDIA_URL': settings.MEDIA_URL,
        })

    return render(request, 'survey/pet_survey.html', {
        'form': form,
    })


<<<<<<< HEAD
=======
def save_matching_result(request):
    # リクエストからペットのIDを取得
    pet_id = request.GET.get('pet_id') or request.POST.get('pet_id')

    # IDの存在確認
    if not pet_id:
        return render(request, 'error.html', {'message': 'ペットIDが正しくありません。'})

    # 該当するペットを取得
    pet = get_object_or_404(Pet, id=pet_id)

    # マッチング履歴を保存
    matching_history = MatchingHistory.objects.create(
        matched_pet=pet
    )

    # 成功時のページを表示
    return render(request, 'matching_success.html', {'history': matching_history})


>>>>>>> 953c8cd2c76ab2f36d4a4acc095ca1bb4550f752
class IndexView(TemplateView):
    """トップページのビュー"""
    template_name = 'Survey/index.html'


def index(request):
    """トップページを表示"""
    return render(request, 'Survey/index.html')
