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

        # pet_type が一致した場合、スコアを加算
        if pet_type:
            pets_data['score'] += (pets_data['type'] == pet_type).astype(int)

        # sex が一致した場合、スコアを加算
        if sex:
            pets_data = pets_data[pets_data['sex'] == sex]
            pets_data['score'] += (pets_data['sex'] == sex).astype(int)

        # 年齢範囲のフィルタリング（年齢条件だけ追加）
        if age_range:
            selected_age_ranges = age_range.split(',')  # カンマで分割して選ばれた範囲をリストに

            # 年齢範囲内のペットにスコアを加算
            if '0-3' in selected_age_ranges:
                pets_data['score'] += (pets_data['age'] <= 3).astype(int)
            if '4-7' in selected_age_ranges:
                pets_data['score'] += ((pets_data['age'] >= 4) & (pets_data['age'] <= 7)).astype(int)
            if '8-10' in selected_age_ranges:
<<<<<<< HEAD
                pets_data['score'] += ((pets_data['age'] >= 8) & (pets_data['age'] <= 10)).astype(int)

        # 年齢範囲内のペットを若い順に並べる
        final_sorted_pets = pets_data.sort_values(by=['score', 'age'], ascending=[False, True])
=======
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
>>>>>>> d8f8acbea35efff972ae63a41fe2587e6c3c286b

        print("スコア計算後のペットデータ:", pets_data[['score']])  # デバッグ用

        # スコアが0のペットと1以上のペットに分ける
        pets_score_0 = final_sorted_pets[final_sorted_pets['score'] == 0]
        pets_score_1_or_more = final_sorted_pets[final_sorted_pets['score'] > 0]

        # 画像URLの処理
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

        print("スコア0のペット:", pet_with_images_score_0)
        print("スコア1以上のペット:", pet_with_images_score_1_or_more)

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
            'pets': pet_with_images_score_1_or_more + pet_with_images_score_0,  # スコア1以上とスコア0を合わせる
            'MEDIA_URL': settings.MEDIA_URL,
        })

    return render(request, 'survey/pet_survey.html', {
        'form': form,
    })


class IndexView(TemplateView):
    """トップページのビュー"""
    template_name = 'Survey/index.html'


def index(request):
    """トップページを表示"""
    return render(request, 'Survey/index.html')
