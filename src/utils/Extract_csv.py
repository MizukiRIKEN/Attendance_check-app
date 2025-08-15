import pandas as pd

# filepath: /Users/mizuki/Documents/Conference/Attendance_check-app/src/extract_example.py

# 登録者リストCSVファイル名
REGISTERED_FILE = "NuSym25_registered.csv"  # 適宜ファイル名を変更

# CSVを読み込む
df = pd.read_csv(REGISTERED_FILE)

filtered_df = df[df['Excursion'].notnull() & df['Name'].notnull()]

# IDと名前だけ抽出
id_name_df = df[['ID', 'Name']]

print(id_name_df)