import pandas as pd
import os
import sys
from config import MEETING_TYPES,REGISTERED_FILE,REGISTERED_HEAD,CHECKIN_HEAD 

# filepath: /Users/mizuki/DocumenEts/Conference/Attendance_check-app/src/extract_example.py

# 登録者リストCSVファイル名
if not os.path.exists(REGISTERED_FILE):
    print(f"登録者リストファイルが見つかりません: {REGISTERED_FILE}")
    sys.exit()
    
# CSVを読み込む
df = pd.read_csv(REGISTERED_FILE)
if df.empty:
    print("登録者リストが空です。")
    sys.exit()

# 登録者リストを抽出する
paied_df = df[df['Name'].notnull() & (df["Registration state"]!="Withdrawn")]
#paied_df = df[df['ID'].notnull()]

for key in MEETING_TYPES:
    REGISTERED_FILE = REGISTERED_HEAD + key + ".csv"
    CHECKIN_FILE = CHECKIN_HEAD + key + ".csv"

    # ExcursionとNameの列がnullでない行を抽出
    if key == "Entrance" or key == "Session":
        filtered_df = paied_df
    elif key == "Going" or key == "Return" or key == "Ropeway":
        skey = "Excursion"
        filtered_df = paied_df[paied_df[skey]=='Yes']
    else:
        skey = key
        filtered_df = paied_df[paied_df[skey]=='Yes']

    if key == "Banquet":
        id_name_df = filtered_df[['ID', 'Name', 'Dietary Request', 'Detail of Dietary Request']]
    elif key == "Session":
        id_name_df = filtered_df[['ID', 'Name','Excursion','Banquet']]
    else:
        id_name_df = filtered_df[['ID', 'Name']]
    
    id_name_df.to_csv(REGISTERED_FILE, index=False)
    print(f"{REGISTERED_FILE} に {len(id_name_df)} 人の登録者がいます。")

