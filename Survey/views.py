import joblib  # type: ignore
from django.shortcuts import render  # type: ignore
from django.views.generic.base import TemplateView  # type: ignore
from .forms import SimplePetSurveyForm
from petapp.models import Pet
from .models import SurveyResult
from sklearn.preprocessing import LabelEncoder  # type: ignore

# モデルのパスを設定
MODEL_PATH = 'C:/Users/t_koitabashi/Desktop/卒業制作/PET/Pet/models/your_trained_model.pkl'

# AIモデルの読み込み
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except FileNotFoundError:
    model = None
    print(f"Model file not found at {MODEL_PATH}")

# カテゴリカルデータを数値に変換するためのラベルエンコーダー
size_encoder = LabelEncoder()


# ラベルエンコーダーを使ってサイズを数値に変換
def encode_size(size):
    try:
        return size_encoder.transform([size])[0]
    except ValueError:
        # ラベルエンコーダーに対応していないサイズが入力された場合
        return 0  # 0でデフォルトの処理を行う


def predict_pet_match_score(pet_data, survey_data):
    """
    survey_data の情報を基に、AIモデルが予測した適合度スコアを返します。
    """
    if model is None:
        raise Exception("AIモデルが読み込まれていません")

    # survey_dataからカテゴリカルデータを数値に変換
    survey_features = [
        len(survey_data['pet_type']), 
        len(survey_data['activity_level']),
        encode_size(survey_data['pet_size_preference']),  # ここでエンコード
        len(survey_data['living_environment']),
        0,  # その他の特徴量（仮）
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 合計20個
    ]
    
    # 20個の特徴量を持つ入力に変換して予測
    score = model.predict([survey_features])[0]
    return score


def pet_survey(request):
    if request.method == 'POST':
        form = SimplePetSurveyForm(request.POST)
        if form.is_valid():
            # アンケートの回答をモデルで扱いやすい形式に変換
            pet_type = form.cleaned_data['pet_type']
            living_environment = form.cleaned_data['living_environment']
            pet_personality = form.cleaned_data['pet_personality']
            activity_level = form.cleaned_data['activity_level']
            pet_size_preference = form.cleaned_data['pet_size_preference']

            # データベースからペットをフィルター
            matched_pets = Pet.objects.all()

            # アンケートデータをAIモデル用に変換
            survey_data = {
                'pet_type': [pet_type],
                'activity_level': [activity_level],
                'pet_size_preference': [pet_size_preference],
                'living_environment': [living_environment]
            }

            # ペットごとの適合度スコアを計算し、スコア順に並び替える
            pet_scores = []
            for pet in matched_pets:
                pet_data = {
                    'type': pet.type,
                    'size': pet.size,
                    'color': pet.color,
                    'age': pet.age,
                }
                score = predict_pet_match_score(pet_data, survey_data)
                pet_scores.append((pet, score))

            # スコア順にソートし、スコアが0.5以上のペットのみを選択
            pet_scores.sort(key=lambda x: x[1], reverse=True)
            matched_pets = [pet for pet, score in pet_scores if score > 0.5]

            # 結果を保存または表示
            if matched_pets:
                survey_result = SurveyResult(
                    pet_type=pet_type,
                    living_environment=living_environment,
                    pet_personality=pet_personality,
                    activity_level=activity_level,
                    pet_size_preference=pet_size_preference
                )
                survey_result.save()
                return render(request, 'survey/results.html',
                              {'matched_pets': matched_pets})
            else:
                return render(request, 'survey/no_results.html',
                              {'form': form})
    else:
        form = SimplePetSurveyForm()

    return render(request, 'survey/pet_survey.html', {'form': form})


class IndexView(TemplateView):
    template_name = 'Survey/index.html'


def index(request):
    return render(request, 'Survey/index.html')
