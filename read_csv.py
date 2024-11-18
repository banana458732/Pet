import pandas as pd

# CSVファイルのパスを指定
<<<<<<< HEAD
csv_file_path = 'C:\\Users\\t_yamanoi\\Documents\\卒業制作\\Pet\\pets_data.csv'
=======
csv_file_path = 'pets_data.csv'
>>>>>>> 8fa17b7960a6b617dcaa4d7ddd6aa9b694d85dc6

# CSVファイルを読み込む
data = pd.read_csv(csv_file_path)

# データの先頭5行を表示
print(data.head())
