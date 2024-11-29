import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import SimplePetSurveyForm
from .models import SurveyResult
from django.http import HttpResponse
from django.conf import settings
from petapp.models import Pet

def pet_survey(request):
    form = SimplePetSurveyForm(request.POST or None)

    # CSVファイルの読み込み
    try:
        pets_data = pd.read_csv('pets_data.csv', encoding='utf-8')
        pets_data = pets_data.fillna('')
    except Exception as e:
        return HttpResponse(f"CSVファイルの読み込みに失敗しました: {e}")

    if request.method == 'POST' and form.is_valid():
        # フォームからの入力データ取得
        pet_type = form.cleaned_data.get('pet_type')
        size = form.cleaned_data.get('size')
        color = form.cleaned_data.get('color')
        kinds = form.cleaned_data.get('kinds')
        disease = form.cleaned_data.get('disease')
        personality = form.cleaned_data.get('pet_personality')
        sex = form.cleaned_data.get('sex')
        age_range = form.cleaned_data.get('age_range')

        # フィルタリング処理
        if pet_type:
            pets_data = pets_data[pets_data['type'] == pet_type]

        # スコア計算
        pets_data['score'] = 0
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
        if pet_type:
            pets_data['score'] += (pets_data['type'] == pet_type).astype(int)
        if sex:
            pets_data = pets_data[pets_data['sex'] == sex]
            pets_data['score'] += (pets_data['sex'] == sex).astype(int)
        if age_range:
            selected_age_ranges = age_range.split(',')
            if '0-3' in selected_age_ranges:
                pets_data['score'] += (pets_data['age'] <= 3).astype(int)
            if '4-7' in selected_age_ranges:
                pets_data['score'] += ((pets_data['age'] >= 4) & (pets_data['age'] <= 7)).astype(int)
            if '8-10' in selected_age_ranges:
                pets_data['score'] += ((pets_data['age'] >= 8) & (pets_data['age'] <= 10)).astype(int)

        # スコアで並べ替え
        final_sorted_pets = pets_data.sort_values(by=['score', 'age'], ascending=[False, True])

        # スコアによる分類
        pets_score_0 = final_sorted_pets[final_sorted_pets['score'] == 0]
        pets_score_1_or_more = final_sorted_pets[final_sorted_pets['score'] > 0]

        # 画像の処理
        pet_with_images_score_0 = []
        pet_with_images_score_1_or_more = []

        for pet in pets_score_0.to_dict('records'):
            image_urls = pet.get('image_urls', '')
            first_image = image_urls.split(',')[0] if image_urls else None
            pet_with_images_score_0.append((pet, first_image))

        for pet in pets_score_1_or_more.to_dict('records'):
            image_urls = pet.get('image_urls', '')
            first_image = image_urls.split(',')[0] if image_urls else None
            pet_with_images_score_1_or_more.append((pet, first_image))

        # スコア1以上のペットがいるかどうかのフラグ
        has_score_above_zero = any(pet['score'] > 0 for pet in pets_score_1_or_more.to_dict('records'))

        # SurveyResult保存
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

        return render(request, 'survey/results.html', {
            'survey_result': survey_result,
            'pets': pet_with_images_score_1_or_more + pet_with_images_score_0,
            'MEDIA_URL': settings.MEDIA_URL,
            'pets_score_0': pets_score_0,
            'has_pets_score_0': len(pets_score_0) > 0,
            'has_score_above_zero': has_score_above_zero,
        })

    return render(request, 'survey/pet_survey.html', {'form': form})

class IndexView(TemplateView):
    """トップページのビュー"""
    template_name = 'Survey/index.html'

def index(request):
    """トップページを表示"""
    return render(request, 'Survey/index.html')
