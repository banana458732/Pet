import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import SimplePetSurveyForm
from .models import SurveyResult
from django.http import HttpResponse
from django.conf import settings
from petapp.models import Pet
from fuzzywuzzy import fuzz
from janome.tokenizer import Tokenizer
import unicodedata


# Janomeトークナイザの初期化
tokenizer = Tokenizer()


# ひらがなに変換する関数
def to_hiragana(text):
    tokens = tokenizer.tokenize(text)
    result = []
    for token in tokens:
        # 読み仮名が取得できる場合はそれを使用
        reading = token.reading if token.reading != "*" else token.surface
        # カタカナをひらがなに変換
        hiragana = unicodedata.normalize('NFKC', reading).translate(
            str.maketrans("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョッー", 
                          "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょっー"))
        result.append(hiragana)
    return ''.join(result)


def pet_survey(request):
    form = SimplePetSurveyForm(request.POST or None)

    # CSVファイルの読み込み
    try:
        pets_data = pd.read_csv('pets_data.csv', encoding='utf-8')
        pets_data = pets_data.fillna('')
    except Exception as e:
        return HttpResponse(f"CSVファイルの読み込みに失敗しました: {e}")

    # CSVデータの性格列をひらがなに変換
    if 'personality' in pets_data.columns:
        pets_data['hiragana_personality'] = pets_data['personality'].apply(to_hiragana)
    else:
        # personality 列がない場合の処理（例えばデフォルト値を設定するなど）
        pets_data['hiragana_personality'] = ''

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

        # 色、品種、病気をひらがなに変換
        input_hiragana_color = to_hiragana(color) if color else ""
        input_hiragana_kinds = to_hiragana(kinds) if kinds else ""
        input_hiragana_disease = to_hiragana(disease) if disease else ""

        # CSVデータの色、品種、病気列をひらがなに変換
        pets_data['hiragana_color'] = pets_data['color'].apply(to_hiragana)
        pets_data['hiragana_kinds'] = pets_data['kinds'].apply(to_hiragana)
        pets_data['hiragana_disease'] = pets_data['disease'].apply(to_hiragana)

        # スコア計算
        pets_data['score'] = 0
        if pet_type:
            pets_data = pets_data[pets_data['type'] == pet_type]
            pets_data['score'] += (pets_data['type'] == pet_type).astype(int)
        if size:
            pets_data['score'] += (pets_data['size'] == size).astype(int)
        if color:
            pets_data['score'] += pets_data['hiragana_color'].apply(lambda x: 1 if input_hiragana_color in x or x in input_hiragana_color else 0)
        if kinds:
            # ひらがなに変換した品種を使用して部分一致を確認
            input_hiragana_kinds = to_hiragana(kinds) if kinds else ""
            pets_data['score'] += pets_data['hiragana_kinds'].apply(
                lambda x: 1 if fuzz.partial_ratio(input_hiragana_kinds, x) > 80 else 0
            )
        if disease:
            # 入力された病歴とCSVデータの病歴に対して部分一致を使用
            pets_data['score'] += pets_data['hiragana_disease'].apply(
                lambda x: 1 if fuzz.partial_ratio(input_hiragana_disease, x) > 80 else 0
            )
        if personality:
            # 性格マッチング処理（スコア計算）
            input_hiragana_personality = to_hiragana(personality) if personality else ""
            pets_data['score'] += pets_data['hiragana_personality'].apply(
                lambda x: 1 if fuzz.partial_ratio(input_hiragana_personality, x) > 70 else 0
            )
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
            first_image = None  # Default to None
            if image_urls:
                first_image = image_urls.split(',')[0]  # Get the first image URL
            pet_with_images_score_0.append((pet, first_image))

        for pet in pets_score_1_or_more.to_dict('records'):
            image_urls = pet.get('image_urls', '')
            first_image = None  # Default to None
            if image_urls:
                first_image = image_urls.split(',')[0]  # Get the first image URL
            pet_with_images_score_1_or_more.append((pet, first_image))

        # フラグ設定
        has_score_above_zero = len(pets_score_1_or_more) > 0
        has_pets_score_0 = len(pets_score_0) > 0
        only_score_0_pets = has_pets_score_0 and not has_score_above_zero

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
            'has_pets_score_0': has_pets_score_0,
            'has_score_above_zero': has_score_above_zero,
            'only_score_0_pets': only_score_0_pets,
        })

    return render(request, 'survey/pet_survey.html', {'form': form})


class IndexView(TemplateView):
    """トップページのビュー"""
    template_name = 'Survey/index.html'


def index(request):
    """トップページを表示"""
    return render(request, 'Survey/index.html')
