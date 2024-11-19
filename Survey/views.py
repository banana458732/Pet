# survey/views.py
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import SimplePetSurveyForm
from .models import SurveyResult, SurveyHistory
from petapp.models import Pet
import pandas as pd



# pets_data.csvからデータを読み込む
def load_pet_data():
    """CSVファイルからペット情報を読み込む"""
    pet_df = pd.read_csv('pets_data.csv')  # CSVファイルのパスを設定
    return pet_df


# ユーザーが入力した自由記述の内容を解析
def parse_user_input(user_input, pet_df):
    """ユーザーの入力を解析して、条件を抽出"""
    # CSVからユニークなキーワードを抽出
    keywords = {
        'type': pet_df['type'].dropna().unique().tolist(),
        'size': pet_df['size'].dropna().unique().tolist(),
        'personality': pet_df['personality'].dropna().unique().tolist(),
        'color': pet_df['color'].dropna().unique().tolist(),
        'disease': pet_df['disease'].dropna().unique().tolist(),
        'sex': pet_df['sex'].dropna().unique().tolist(),
        'syu': pet_df['syu'].dropna().unique().tolist(),
    }

    # 初期条件を設定
    conditions = {
        'type': None,
        'size': None,
        'personality': None,
        'color': None,
        'disease': None,
        'sex': None,  # sexを追加
        'syu': None   # syuを追加
    }

    # ユーザー入力が文字列であるかを確認し、小文字に変換
    if isinstance(user_input, str):
        user_input = user_input.lower()
    else:
        user_input = ""  # 文字列でない場合は空文字列にする

    # ユーザーの入力に基づいて条件を探す
    for key, values in keywords.items():
        for value in values:
            if isinstance(value, str) and value.lower() in user_input:  # 入力とキーワードを小文字で比較
                conditions[key] = value  # マッチした場合、条件を更新

    return conditions


def age_filter(age_ranges, pet_df):
    """選択された年齢範囲に基づいてフィルタリング"""
    if not age_ranges:
        return None  # 年齢範囲が指定されていない場合はフィルタなし

    filters = []
    for age_range in age_ranges:
        if age_range == '0-3':
            filters.append((pet_df['age'] >= 0) & (pet_df['age'] <= 3))
        elif age_range == '4-7':
            filters.append((pet_df['age'] >= 4) & (pet_df['age'] <= 7))
        elif age_range == '8-10':
            filters.append((pet_df['age'] >= 8) & (pet_df['age'] <= 10))

    if filters:
        # 複数の条件をORで結合して返す
        combined_filter = filters[0]
        for filter_cond in filters[1:]:
            combined_filter |= filter_cond  # 各条件をORで結合
        return combined_filter
    return None


def pet_survey(request):
    """ペットアンケートに基づいてペット情報をフィルタリングし表示"""
    if request.method == 'POST':
        form = SimplePetSurveyForm(request.POST)
        if form.is_valid():
            # フォームからのユーザー入力
            user_input = form.cleaned_data.get('general_info', '')  # 'general_info'がフォームに存在することを確認
            selected_age_ranges = form.cleaned_data.get('age_range', [])

            # ペット情報のCSVを読み込む
            pet_df = load_pet_data()

            # ユーザー入力を解析して条件を抽出
            conditions = parse_user_input(user_input, pet_df)

            # フィルタリング条件を構築
            filters = []
            for column, value in conditions.items():
                if value is not None:
                    filters.append(pet_df[column] == value)  # 各列の値が条件と一致するかをチェック

            # 年齢範囲のフィルタを追加
            age_conditions = age_filter(selected_age_ranges, pet_df)
            if age_conditions is not None:
                filters.append(age_conditions)  # 複数の年齢範囲条件を追加

            # フィルタリング条件を全てANDで結合
            if filters:
                combined_filter = filters[0]
                for filter_cond in filters[1:]:
                    combined_filter &= filter_cond  # 各条件をANDで結合
                # 条件に基づいてペット情報をフィルタリング
                matching_pets = pet_df[combined_filter]
            else:
                # 条件が何もない場合はすべてのペットを返す
                matching_pets = pet_df

            # 結果を表示
            if not matching_pets.empty:
                # SurveyResultを作成し、マッチングペットを保存
                survey_result = SurveyResult.objects.create(
                    pet_type=conditions['type'] or '',
                    size=conditions['size'] or '',
                    color=conditions['color'] or '',
                    age=','.join(selected_age_ranges) or '',
                    pet_personality=form.cleaned_data.get('personality', '') or '',
                    activity_level=form.cleaned_data.get('activity_level', '') or '',
                    pet_size_preference=form.cleaned_data.get('pet_size_preference', '') or '',
                    additional_requests=form.cleaned_data.get('additional_requests', '') or '',
                )

                # ユーザーの過去のアンケート結果を取得
                user_history = SurveyHistory.objects.filter(user=request.user).order_by('-date_created')

                # 過去のマッチング履歴をPetテーブルから取得
                matched_pets = Pet.objects.filter(
                    id__in=user_history.values_list('matched_pet_id', flat=True)
                )

                # 結果を表示
                return render(request, 'survey/results.html', {
                    'matching_pets': matching_pets.to_dict(orient='records'),
                    'survey_result': survey_result,
                    'user_history': user_history,  # ユーザーの過去の履歴を渡す
                    'matched_pets': matched_pets  # Petテーブルから取得した過去のマッチングペット情報を渡す
                })
            else:
                return render(request, 'survey/no_results.html', {'form': form})
    else:
        form = SimplePetSurveyForm()

    # ユーザーの過去のアンケート結果を取得
    user_history = SurveyHistory.objects.filter(user=request.user).order_by('-date_created')

    return render(request, 'survey/pet_survey.html', {
        'form': form,
        'user_history': user_history  # ユーザーの過去の履歴を渡す
    })


class IndexView(TemplateView):
    """トップページのビュー"""
    template_name = 'Survey/index.html'


def index(request):
    """トップページを表示"""
    return render(request, 'Survey/index.html')


# 過去の履歴詳細ページのビュー
def history_detail(request, id):
    """過去のアンケート結果詳細を表示"""
    # IDに対応する履歴を取得
    try:
        history = SurveyHistory.objects.get(id=id)  # IDに該当する履歴データを取得
    except SurveyHistory.DoesNotExist:
        history = None  # 履歴が存在しない場合はNoneを返す（エラーハンドリング）

    return render(request, 'survey/history_detail.html', {'history': history})
