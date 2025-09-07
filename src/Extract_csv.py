import pandas as pd
import os
import sys
from config import *

# Excelファイルからシートを読み込む
dd = pd.read_excel(ORIGINAL_DATABASE, sheet_name=DATABASE_SHEET)
# CSVファイルとして保存
dd.to_csv(PARTICIPANT_LIST, index=False, encoding='utf-8-sig')
print(f"{DATABASE_SHEET} を {PARTICIPANT_LIST} に保存しました。")

#sys.exit()

# 登録者リストCSVファイル名
if not os.path.exists(PARTICIPANT_LIST):
    print(f"登録者リストファイルが見つかりません: {PARTICIPANT_LIST}")
    sys.exit()
    
# CSVを読み込む
df = pd.read_csv(PARTICIPANT_LIST)
if df.empty:
    print("登録者リストが空です。")
    sys.exit()

# 登録者リストを抽出する
paied_df = df[df['Name'].notnull() & (df["Registration state"]!="Withdrawn")]
#paied_df = df[df['ID'].notnull()]

for key in MEETING_TYPES:
    REGISTERED_FILE = f"{DIR_OUTPUT}/{REGISTERED_HEAD}{key}.csv"
    CHECKIN_FILE = f"{DIR_OUTPUT}/{CHECKIN_HEAD}{key}.csv"

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
        id_name_df = filtered_df[['ID', 'Name','Excursion','Banquet','Dietary Request']].copy()  # ← .copy() を追加
        id_name_df['Time'] = ''
        id_name_df['Comment'] = ''
        id_name_df['Receptionist'] = ''
    else:
        id_name_df = filtered_df[['ID', 'Name']]
    
    id_name_df.to_csv(REGISTERED_FILE, index=False)
    print(f"{REGISTERED_FILE} に {len(id_name_df)} 人の登録者がいます。")

# filepath: /Users/mizuki/Documents/Conference/Attendance_check-app/src/extract_sheet.py

