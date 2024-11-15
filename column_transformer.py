# import pandas as pd
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.impute import SimpleImputer
# import joblib

# # CSVファイルを読み込む
# df = pd.read_csv('pets_data.csv')

# # 不要なカラムを削除
# df = df.drop(columns=['Unnamed: 9'], errors='ignore')

# # ColumnTransformerで前処理のステップを設定
# column_transformer = ColumnTransformer(
#     transformers=[
#         ('num', SimpleImputer(strategy='mean'), ['age']),
#         ('cat', OneHotEncoder(), ['type', 'size', 'color', 'syu', 'personality', 'sex']),
#         ('imp', SimpleImputer(strategy='constant', fill_value='unknown'), ['disease'])
#     ], remainder='passthrough'
# )

# # データ変換の実行
# X_transformed = column_transformer.fit_transform(df)

# # ColumnTransformerを保存
# joblib.dump(column_transformer, 'column_transformer.pkl')

# print("変換後のデータ:")
# print(X_transformed)
