import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import SimplePetSurveyForm
from .models import SurveyResult
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Pet

def pet_survey(request):
    form = SimplePetSurveyForm(request.POST or None)

    # CSVファイルの読み込み
    try:
        pets_data = pd.read_csv('pets_data.csv', encoding='utf-8')  # pets_data.csvを読み込む
    except Exception as e:
        return HttpResponse(f"CSVファイルの読み込みに失敗しました: {e}")

    # フォームが送信された場合、マッチ率に基づいてペットをフィルタリング
    if request.method == 'POST' and form.is_valid():
        # フォームから取得するフィールド
        pet_type = form.cleaned_data.get('pet_type')
        size = form.cleaned_data.get('size')
        color = form.cleaned_data.get('color')
        kinds = form.cleaned_data.get('kinds')
        disease = form.cleaned_data.get('disease')
        personality = form.cleaned_data.get('pet_personality')  # 修正: pet_personality → personality
        sex = form.cleaned_data.get('sex')
        age_range = form.cleaned_data.get('age_range')  # age_rangeを取得

        # フィルタリング条件に一致するペットを取得
        filtered_pets = pets_data.copy()

        if pet_type:
            filtered_pets = filtered_pets[filtered_pets['type'] == pet_type]
        if size:
            filtered_pets = filtered_pets[filtered_pets['size'] == size]
        if color:
            filtered_pets = filtered_pets[filtered_pets['color'] == color]
        if kinds:
            filtered_pets = filtered_pets[filtered_pets['kinds'] == kinds]
        if disease:
            filtered_pets = filtered_pets[filtered_pets['disease'] == disease]
        if personality:  # 修正: pet_personality → personality
            filtered_pets = filtered_pets[filtered_pets['personality'] == personality]  # 修正: pet_personality → personality
        if sex:
            filtered_pets = filtered_pets[filtered_pets['sex'] == sex]

        # 年齢範囲に基づくフィルタリング
        if age_range:
            if '0-3' in age_range:
                filtered_pets = filtered_pets[filtered_pets['age'] <= 3]
            if '4-7' in age_range:
                filtered_pets = filtered_pets[(filtered_pets['age'] >= 4) & (filtered_pets['age'] <= 7)]
            if '8-10' in age_range:
                filtered_pets = filtered_pets[(filtered_pets['age'] >= 8) & (filtered_pets['age'] <= 10)]

        # マッチング結果をリスト化
        sorted_pets = filtered_pets.to_dict('records')  # フィルタリング後のデータを辞書形式で取得
        pet_with_images = [(pet, pet['image_urls']) for pet in sorted_pets]

        # SurveyResultを作成し、マッチング結果を保存
        survey_result = SurveyResult.objects.create(
            pet_type=pet_type or '',
            size=size or '',
            color=color or '',
            kinds=kinds or '',
            disease=disease or '',
            pet_personality=personality or '',  # 修正: pet_personality → personality
            sex=sex or '',
            age_range=", ".join(age_range) if age_range else ''  # age_rangeも保存
        )

        # 結果ページをレンダリングして返す
        return render(request, 'survey/results.html', {
            'survey_result': survey_result,
            'pets': pet_with_images,  # 修正: 'pets' という名前で渡す
            'MEDIA_URL': settings.MEDIA_URL,  # 画像URLに対応
        })

    # 初期表示用（フィルタリングしないすべてのペット）
    return render(request, 'survey/pet_survey.html', {
        'form': form,
    })

class IndexView(TemplateView):
    """トップページのビュー"""
    template_name = 'Survey/index.html'


def index(request):
    """トップページを表示"""
    return render(request, 'Survey/index.html')
