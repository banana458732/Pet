# import os
# import joblib  # type: ignore
# import pandas as pd  # type: ignore
# from sklearn.ensemble import RandomForestClassifier  # type: ignore
# from sklearn.model_selection import train_test_split  # type: ignore
# from sklearn.metrics import accuracy_score  # type: ignore
# from petapp.models import Pet

# # Petモデルからデータを取得
# data = Pet.objects.all()

# # DataFrameに変換し、必要なフィールドを抽出
# df = pd.DataFrame(list(data.values('size', 'age', 'personality', 'type')))

# # personalityフィールドの欠損値を埋める
# df['personality'] = df['personality'].fillna('Unknown')

# # 特徴量とターゲット変数を設定
# X = df[['size', 'age', 'personality']]
# y = df['type']

# # カテゴリカルデータの数値エンコード
# X = pd.get_dummies(X)

# # データをトレーニングセットとテストセットに分ける
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # モデルのトレーニング
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # モデルの評価
# y_pred = model.predict(X_test)
# print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# # モデルの保存
# model_dir = os.path.join(os.getcwd(), 'Pet', 'models')
# if not os.path.exists(model_dir):
#     os.makedirs(model_dir)

# model_path = os.path.join(model_dir, 'your_trained_model.pkl')
# joblib.dump(model, model_path)
# print(f"Model saved as {model_path}")
