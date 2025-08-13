import streamlit as st
from utils import *  # ユーティリティ関数をインポート
from types import *  # 型定義をインポート
import pandas as pd
from datetime import datetime
import os
from config import MEETING_TYPES

#%%----  
def diffrentiate_checkin(cid,CHECKIN_FILE):
    """
    チェックインの差分を表示する関数
    """
    log_df = pd.read_csv(CHECKIN_FILE)
    fuser = log_df[log_df['ID'] == int(cid)]
    if fuser.empty:
        st.write(f"ID {cid} 新チェックイン")
        return True
    else:
        st.error(f"ID {cid} : {fuser} チェックイン済み")
        return False
#%%----
# チェクインしていない参加者のリストを表示
def show_not_checked_in_participants(df,CHECKIN_FILE):
    if not os.path.exists(CHECKIN_FILE):
        return
    
    registered_ids = set(df['ID'].astype(str).str.strip())
    checked_in_ids = set(pd.read_csv(CHECKIN_FILE, usecols=[0], names=["ID"])['ID'].astype(str).str.strip())
    
    not_checked_in = registered_ids - checked_in_ids
    not_checked_in_sorted = sorted([int(x) for x in not_checked_in])
    not_checked_in = set(map(str, not_checked_in_sorted))
    
    if not not_checked_in:
        st.info("全ての参加者がチェックイン済みです。")
    else:
        st.write("未チェックインの参加者ID:")
        st.write(f"Rest {len(not_checked_in)} persons:")
        st.write(f" {not_checked_in_sorted}")

    
#%%----
# チェックインログを表示するボタン
def show_checkin_log(CHECKIN_FILE):
    if not os.path.exists(CHECKIN_FILE):
        return
    
    if CHECKIN_FILE:
        st.write(f"チェックインログ [{CHECKIN_FILE}]")
        log_df = pd.read_csv(CHECKIN_FILE)
        st.write(log_df)   
    else:
        st.error("チェックインログが見つかりません。")
        
    
#%%----
def main():
    st.title("NuSym25")
    st.write("NuSym25参加者を確認するアプリです。")

    meeting_type = st.selectbox(
        "リストの種類を選択してください",
        options=MEETING_TYPES,
        index=1  # デフォルトで最初のオプションを選択
    )
    
    REGISTERED_HEAD = "Registered_"
    CHECKIN_HEAD = "Checkin_"
    REGISTERED_FILE = REGISTERED_HEAD + meeting_type + ".csv"
    CHECKIN_FILE = CHECKIN_HEAD + meeting_type + ".csv"
    st.write(f" {meeting_type} を選択中")
   
    # CSVファイルから登録者リストを読み込

    if not os.path.exists(REGISTERED_FILE):
        st.error(f"登録者リストファイルが見つかりません: {REGISTERED_FILE}")
        return  
    
    df = pd.read_csv(REGISTERED_FILE, dtype={"id": int, "name": str})
    if df.empty:
        st.error("登録者リストが空です。")
        return
    
    if not os.path.exists(CHECKIN_FILE):
        st.write(f"チェックイン記録ファイルが見つかりません: {CHECKIN_FILE}")
        st.write("新しいチェックインを開始します。")
        with open(CHECKIN_FILE, "w") as f:
            f.write("ID,Name,Time\n")
    
   
    st.markdown(f'<span style="color:blue"> 登録者リストファイル: [{REGISTERED_FILE}]</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="color:blue"> チェックイン記録ファイル: [{CHECKIN_FILE}]</span>', unsafe_allow_html=True)
    st.markdown("---")


    st.title("✅ 出席確認アプリ")
    st.write(f"参加者リストファイル: [{REGISTERED_FILE}]")

    # 入力フォーム
    input_id = st.text_input("参加者IDを入力してください", placeholder="例: 12")


    input_id = input_id.strip()  # 前後の空白を削除

    if st.button("出席確認"):
        if input_id:
            # IDが登録者リストに存在するか確認
            user = df[df['ID'] == int(input_id)]
            #st.write(user)
        
            if not user.empty:
                name = user.iloc[0]['Name']
                st.write(f"[{input_id}] 参加者: {name} さん")
            
                if diffrentiate_checkin(input_id,CHECKIN_FILE):
                
                    st.success(f"{name} さんの出席を確認しました ✅")
                    # チェックイン記録を保存
                    with open(CHECKIN_FILE, "a") as f:
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 秒まで
                        f.write(f"{input_id},{name},{now_str}\n")
                else:
                    st.warning(f"{name} さんはすでにチェックイン済みです。")
            else:
                st.error("未登録のIDです。")
        else:
            st.warning("IDを入力してください。")

    st.markdown("---")

    show_not_checked_in_participants(df, CHECKIN_FILE)

    show_checkin_log(CHECKIN_FILE)        
    
    
    st.markdown("---")
    # チェックインログのダウンロードボタン
    now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    st.write("チェックインログをCSV形式でダウンロードできます。")
    st.download_button(
        label=f"{CHECKIN_FILE}をダウンロード",
        data=open(CHECKIN_FILE, "rb").read(),
        file_name=f"{CHECKIN_HEAD}{meeting_type}_{now_str}.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    # チェックインログをアップロードするボタン
 #   st.write("チェックインログをアップロードできます。(運用テスト中)")
 #   uploaded_file = st.file_uploader("チェックインログをアップロード", type=["csv"])
 #   if uploaded_file is not None:
 #       try:
 #           # アップロードされたCSVファイルを読み込む
 #           uploaded_df = pd.read_csv(uploaded_file)
 #           st.write("アップロードされたチェックインログ:")
 #           st.write(uploaded_df)
 #           
 #           # チェックインログを保存
 #           with open(CHECKIN_FILE, "wb") as f:
 #               f.write(uploaded_file.getbuffer())
 #           st.success(f"チェックインログが保存されました: {CHECKIN_FILE}")
 #       except Exception as e:
 #           st.error(f"ファイルの読み込みに失敗しました: {e}")
 #   else:
 #       st.info("アップロードするチェックインログファイルを選択してください。") 
    
    
    

#%%----


if __name__ == "__main__":
    main()