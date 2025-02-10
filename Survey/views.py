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
from karikeiyaku.models import Karikeiyaku

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


from django.core.paginator import Paginator

def pet_survey(request):
    form = SimplePetSurveyForm(request.POST or None)

    # セッションからフォームデータと検索結果を復元
    pets_data = request.session.get('pets_data')

    # セッションデータをDataFrameに変換
    if 'pets_data' in request.session:
        pets_data = pd.DataFrame(request.session['pets_data'])
    else:
        pets_data = None  # セッションにデータがない場合は None にする

    # CSVファイルの読み込み
    try:
        pets_data = pd.read_csv('pets_data.csv', encoding='utf-8')
        pets_data = pets_data.fillna('')  # NaNを空文字に置換
    except Exception as e:
        return HttpResponse(f"CSVファイルの読み込みに失敗しました: {e}")

    # 必要な列をひらがなに変換
    pets_data['hiragana_personality'] = pets_data['personality'].apply(to_hiragana)
    pets_data['hiragana_color'] = pets_data['color'].apply(to_hiragana)
    pets_data['hiragana_kinds'] = pets_data['kinds'].apply(to_hiragana)
    pets_data['hiragana_disease'] = pets_data['disease'].apply(to_hiragana)

    # 仮契約中・契約済みのペットを除外
    pet_ids_to_exclude = Karikeiyaku.objects.filter(
        status__in=['仮契約中', '契約済み']
    ).values_list('pet_id', flat=True)  # ここが 'pet_id' で正しいことを確認

    pets_data = pets_data[~pets_data['id'].isin(pet_ids_to_exclude)]  # 'id'はCSVのフィールド名

    if request.method == 'POST' and form.is_valid():
        # フォーム入力データを取得
        pet_type = form.cleaned_data.get('pet_type')
        size = form.cleaned_data.get('size')
        color = form.cleaned_data.get('color')
        kinds = form.cleaned_data.get('kinds')
        disease = form.cleaned_data.get('disease')
        personality = form.cleaned_data.get('pet_personality')
        sex = form.cleaned_data.get('sex')
        age_range = form.cleaned_data.get('age_range')

        # 入力データをひらがなに変換
        input_hiragana_color = to_hiragana(color) if color else ""
        input_hiragana_kinds = to_hiragana(kinds) if kinds else ""
        input_hiragana_disease = to_hiragana(disease) if disease else ""
        input_hiragana_personality = to_hiragana(personality) if personality else ""

        # スコア計算
        pets_data['score'] = 0

        # ペットタイプ（犬 or 猫）でフィルタリングし、必ずスコア1を加算
        if pet_type:
            pets_data = pets_data[pets_data['type'] == pet_type]
            pets_data['score'] += 1

        # その他条件でスコア計算
        if size:
            pets_data['score'] += (pets_data['size'] == size).astype(int)
        if color:
            pets_data['score'] += pets_data['hiragana_color'].apply(
                lambda x: 1 if input_hiragana_color in x or x in input_hiragana_color else 0
            )
        if kinds:
            pets_data['score'] += pets_data['hiragana_kinds'].apply(
                lambda x: 1 if fuzz.partial_ratio(input_hiragana_kinds, x) > 80 else 0
            )
        if disease:
            pets_data['score'] += pets_data['hiragana_disease'].apply(
                lambda x: 1 if fuzz.partial_ratio(input_hiragana_disease, x) > 80 else 0
            )
        if personality:
            pets_data['score'] += pets_data['hiragana_personality'].apply(
                lambda x: 1 if fuzz.partial_ratio(input_hiragana_personality, x) > 70 else 0
            )
        if sex:
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
        pets_data = pets_data.sort_values(by=['score', 'age'], ascending=[False, True])

        # スコア1以上のペット
        pets_with_score = pets_data[pets_data['score'] >= 1]

        # 分岐処理
        if not pets_with_score.empty:
            if not size and not color and not kinds and not disease and not personality and not sex and not age_range:
                latest_pets = pets_with_score
            else:
                if pets_with_score['score'].max() == 1 and len(pets_with_score) == len(pets_data):
                    latest_pets = pets_data.head(3)
                else:
                    latest_pets = pets_with_score
        else:
            latest_pets = None  # 条件に一致するペットがなければ None にする
        
        # 検索結果をセッションに保存
        request.session['pets_data'] = pets_data.to_dict('records')

        # ページネーション
        paginator = Paginator(latest_pets, 10)  # 1ページに表示する件数
        page_number = request.GET.get('page')  # URLからページ番号を取得
        page_obj = paginator.get_page(page_number)
        

        # 画像の処理
        pets_with_images = []
        for pet in page_obj.object_list.to_dict('records'):
            image_urls = pet.get('image_urls', '')
            first_image = image_urls.split(',')[0] if image_urls else None
            pets_with_images.append((pet, first_image))

        return render(request, 'survey/results.html', {
            'form': form,
            'pets': pets_with_images,
            'page_obj': page_obj,
            'MEDIA_URL': settings.MEDIA_URL,
        })

    return render(request, 'survey/pet_survey.html', {
        'form': form,
    })


def results(request):
    # セッションからフォームデータと検索結果を取得
    form_data = request.session.get('form_data', None)
    pets_data = request.session.get('pets_data', None)

    # フォームデータがある場合、フォームを復元
    form = SimplePetSurveyForm(form_data) if form_data else SimplePetSurveyForm()

    # 検索結果がない場合でもページネーションを表示させるために空のリストを渡す
    if not pets_data:
        pets_data = []  # 空のリストを渡すことで、ページネーションリンクが表示されるようにする

    # ページネーション処理 (1ページ10件)
    paginator = Paginator(pets_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 最後のページが表示されない場合を考慮して、ページネーションのリンクを調整
    if page_obj.number == paginator.num_pages:
        page_obj.has_next = False  # 最後のページでは次ページリンクが出ないように

    # 画像処理 (最初の画像を取得)
    pets_with_images = []
    for pet in page_obj.object_list:
        image_urls = pet.get('image_urls', '')
        first_image = image_urls.split(',')[0] if image_urls else None
        pets_with_images.append((pet, first_image))

    return render(request, 'survey/results.html', {
        'form': form,
        'pets': pets_with_images,
        'page_obj': page_obj,
    })
