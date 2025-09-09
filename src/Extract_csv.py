import pandas as pd
import os
import sys
from config import *

FROM_EXEL = False
if FROM_EXEL:
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
        
CHECKED_LIST = "2025-09-09T05-26_export.csv"
df = pd.read_csv(CHECKED_LIST, dtype=dtype_dict)
if df.empty:
    print("出席者リストが空です。")
    sys.exit()
    

# 登録者リストを抽出する
if FROM_EXEL:
    paied_df = df[df['Name'].notnull() & (df["Registration state"]!="Withdrawn")]
#paied_df = df[df['ID'].notnull()]
else:
    paied_df = df[df['Time'].notnull()]
    total_participants = len(df)
    restofparticipants = len(paied_df)
    print(f"全登録者数: {total_participants}人, 出席者数: {restofparticipants}人, 欠席者数: {total_participants - restofparticipants}人")
                             

for key in MEETING_TYPES:

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
        if FROM_EXEL:
            id_name_df = filtered_df[['ID', 'Name', 'Dietary Request', 'Detail of Dietary Request']]
        else:
            id_name_df = filtered_df[['ID', 'Name','Dietary Request']].copy()
            id_name_df['Detail of Dietary Request'] = ''
    elif key == "Session":
        id_name_df = filtered_df[['ID', 'Name','Excursion','Banquet','Dietary Request']].copy()  # ← .copy() を追加
        id_name_df['Time'] = ''
        id_name_df['Comment'] = ''
        id_name_df['Receptionist'] = ''
        key = "Updated_Session"        
    else:
        id_name_df = filtered_df[['ID', 'Name']]
    
    REGISTERED_FILE = f"{DIR_OUTPUT}/{REGISTERED_HEAD}{key}.csv"
    #CHECKIN_FILE = f"{DIR_OUTPUT}/{CHECKIN_HEAD}{key}.csv"
    id_name_df.to_csv(REGISTERED_FILE, index=False)
    print(f"{REGISTERED_FILE} に {len(id_name_df)} 人の登録者がいます。")

# filepath: /Users/mizuki/Documents/Conference/Attendance_check-app/src/extract_sheet.py

