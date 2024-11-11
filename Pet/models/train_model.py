import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from django.db import models

# Djangoのモデルからデータを取得（SurveyResultモデルを例に）
from survey.models import SurveyResult

# SurveyResultモデルからデータを取得
data = SurveyResult.objects.all()

# データフレームに変換
df = pd.DataFrame(list(data.values('living_environment', 'pet_personality', 'activity_level', 
                                   'pet_size_preference', 'age', 'pet_type')))

# 特徴量とターゲット変数を設定
X = df[['living_environment', 'pet_personality', 'activity_level', 
        'pet_size_preference', 'age']]  # 特徴量
y = df['pet_type']  # ターゲット変数

# カテゴリカルデータを数値に変換
X = pd.get_dummies(X)

# データをトレーニングセットとテストセットに分ける
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデルのトレーニング
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# モデルの評価
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# モデルの保存
model_path = 'C:\\Users\\t_koitabashi\\Desktop\\卒業制作\\PET\\Pet\\models\\your_trained_model.pkl'
joblib.dump(model, model_path)
print(f"Model saved as {model_path}")
