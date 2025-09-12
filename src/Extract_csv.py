import pandas as pd
import os
import sys
from config import *


def extract_registration_list(ORIGINAL_DATABASE, DATABASE_SHEET, PARTICIPANT_LIST):
    # Excelファイルからシートを読み込む
    if not os.path.exists(ORIGINAL_DATABASE):
        print(f"元のEXCELファイルが見つかりません: {ORIGINAL_DATABASE}")
        return False
    
    if PARTICIPANT_LIST and os.path.exists(PARTICIPANT_LIST):
        print(f"出席者リストファイルはすでに存在します: {PARTICIPANT_LIST}")
        return False
          
    df = pd.read_excel(ORIGINAL_DATABASE, sheet_name=DATABASE_SHEET)

    if df.empty:
        print("元データが空です。")
        return False


    attend_df = df[df['Name'].notnull() & (df[REGISTRATION_STATUS_KEYS[0]] != REGISTRATION_STATUS_KEYS[1])]

    id_name_df = attend_df[REGISTRATION_COLUMNS].copy()  # ← .copy() を追加
    id_name_df['Time'] = ''
    id_name_df['Comment'] = ''
    id_name_df['Receptionist'] = ''
    
    id_name_df.to_csv(PARTICIPANT_LIST, index=False)
    print(f"{PARTICIPANT_LIST} に {len(id_name_df)} 人の登録者がいます。")

    return True
#%%%
#　チェックインしたリストから参加確認リストを作成します。
def extract_checking_list(CHECKED_LIST):
    if not os.path.exists(CHECKED_LIST):
        print(f"出席者リストファイルが見つかりません: {CHECKED_LIST}")
        return False
        
    # CSVを読み込む         
    df = pd.read_csv(CHECKED_LIST, dtype=dtype_dict)
    if df.empty:
        print("出席者リストが空です。")
        return False
    
    paied_df = df[df['Time'].notnull()]
    total_participants = len(df)
    restofparticipants = len(paied_df)
    print(f"全登録者数: {total_participants}人, 出席者数: {restofparticipants}人, 欠席者数: {total_participants - restofparticipants}人")

    for key in MEETING_TYPES:

        # ExcursionとNameの列がnullでない行を抽出
        if key == "Going" or key == "Return" or key == "Ropeway":
            skey = "Excursion"
            filtered_df = paied_df[paied_df[skey]=='Yes']
        else:
            skey = key
            filtered_df = paied_df[paied_df[skey]=='Yes']

        if key == "Banquet":
            id_name_df = filtered_df[['ID', 'Name', 'Dietary Request', 'Detail of Dietary Request']]
        else:
            id_name_df = filtered_df[['ID', 'Name']].copy()
    
        REGISTERED_FILE = f"{DIR_OUTPUT}/{REGISTERED_HEAD}{key}.csv"
        #CHECKIN_FILE = f"{DIR_OUTPUT}/{CHECKIN_HEAD}{key}.csv"
        id_name_df.to_csv(REGISTERED_FILE, index=False)
        print(f"{REGISTERED_FILE} に {len(id_name_df)} 人の登録者がいます。")
    
    return True

#%%
def main(FROM_EXCEL):

    if FROM_EXCEL:
        if not extract_registration_list(ORIGINAL_DATABASE, DATABASE_SHEET, PARTICIPANT_LIST):
            sys.exit()
    else:
        if not extract_checking_list(CHECKED_LIST):
            sys.exit()
            
    print("完了")

#%%----
if __name__ == "__main__":
    # コマンドライン引数で切り替え
    # 例: python Extract_csv.py 1  → Excelから
    #     python Extract_csv.py 0  → 既存CSVから
    if len(sys.argv) > 1:
        flag = bool(int(sys.argv[1]))
    else:
        flag = True  # デフォルトはExcelから
    main(flag)
