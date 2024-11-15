import pandas as pd

# CSVファイルのパスを指定
csv_file_path = 'pets_data.csv'

# CSVファイルを読み込む
data = pd.read_csv(csv_file_path)

# データの先頭5行を表示
print(data.head())
