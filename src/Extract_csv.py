import pandas as pd
import os
import sys
from config import MEETING_TYPES, REGISTERED_HEAD, CHECKIN_HEAD

# filepath: /Users/mizuki/DocumenEts/Conference/Attendance_check-app/src/extract_example.py

# 登録者リストCSVファイル名
REGISTERED_FILE = "NuSym25_registered.csv"  # 適宜ファイル名を変更
if not os.path.exists(REGISTERED_FILE):
    print(f"登録者リストファイルが見つかりません: {REGISTERED_FILE}")
    sys.exit()
    
# CSVを読み込む
df = pd.read_csv(REGISTERED_FILE)
if df.empty:
    print("登録者リストが空です。")
    sys.exit()



for key in MEETING_TYPES:
    REGISTERED_FILE = REGISTERED_HEAD + key + ".csv"
    CHECKIN_FILE = CHECKIN_HEAD + key + ".csv"

    
    # ExcursionとNameの列がnullでない行を抽出
    if key == "Goto" or key == "Return":
        skey = "Excursion"
    else:
        skey = key
    filtered_df = df[df[skey]==True & df['Name'].notnull()]
    id_name_df = filtered_df[['ID', 'Name']]
    id_name_df.to_csv(REGISTERED_FILE, index=False)
    print(f"{REGISTERED_FILE} に {len(id_name_df)} 人の登録者がいます。")

