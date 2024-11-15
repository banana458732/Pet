# import pandas as pd
# import joblib

# # 1. 保存した列順を読み込む
# columns_order = joblib.load('columns_order.pkl')

# # 2. 新しいデータを読み込む（仮に新しいデータをdf_newとして）
# df_new = pd.read_csv('pets_data.csv')

# # 3. カテゴリ変数をダミー変数に変換（元のデータと一致させる）
# df_new_encoded = pd.get_dummies(df_new)

# # 4. 学習時の特徴量と新しいデータの特徴量が一致するように順番を合わせる
# df_new_encoded = df_new_encoded.reindex(columns=columns_order, fill_value=0)

# # 5. モデルを読み込む
# model = joblib.load('pet_personality_model.pkl')

# # 6. 予測を行う
# y_new_pred = model.predict(df_new_encoded)

# # 7. 予測結果の表示
# print("予測結果:", y_new_pred)
