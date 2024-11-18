# import pandas as pd
# import joblib

# # 保存した列順を読み込む
# columns_order = joblib.load('columns_order.pkl')

# # 新しいデータを読み込む（仮に新しいデータをdf_newとして）
# df_new = pd.read_csv('pets_data.csv')

# # カテゴリ列を明示的に指定してダミー変数を作成
# # ここでは「type」「size」「color」「syu」「disease」「sex」「personality」などを指定
# df_new_encoded = pd.get_dummies(df_new, columns=['type', 'size', 'color', 'syu', 'disease', 'sex', 'personality'])

# # 訓練時に使用した特徴量の順番に列を並べる
# df_new_encoded = df_new_encoded[columns_order]

# # モデルを読み込む
# model = joblib.load('pet_personality_model.pkl')

# # 予測を行う
# y_new_pred = model.predict(df_new_encoded)

# # 予測結果を表示
# print(y_new_pred)
