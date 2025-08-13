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
        #st.write(f"ID {cid} 新チェックイン")
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
        st.markdown("##### 未チェックインの参加者ID:")
        st.markdown(f"##### 残り {len(not_checked_in)} 人")
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
            f.write("ID,Name,Comment,Time\n")
    
   
    st.markdown(f'<span style="color:blue"> 登録者リストファイル: [{REGISTERED_FILE}]</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="color:blue"> チェックイン記録ファイル: [{CHECKIN_FILE}]</span>', unsafe_allow_html=True)
    st.markdown("---")


    st.title("✅ 出席確認アプリ")
    st.write(f"参加者リストファイル: [{REGISTERED_FILE}]")

    # 入力フォームi
    st.markdown("#### 出席登録する参加者のIDを入力してください")
    input_id = st.text_input("参加者IDを入力してください", placeholder="例: 12")
    comment = st.text_input("コメント（任意）", placeholder="例: 領収書 など")  # ← コメント欄を追加

  

    input_id = input_id.strip()  # 前後の空白を削除

    if st.button("出席確認"):
        if input_id:
            # IDが登録者リストに存在するか確認
            user = df[df['ID'] == int(input_id)]
            #st.write(user)
        
            if not user.empty:
                name = user.iloc[0]['Name']
                st.write(f" 参加者: [{input_id}]　{name} さん")
            
                if diffrentiate_checkin(input_id,CHECKIN_FILE):
                
                    st.success(f"{name} さんの出席を確認しました ✅")
                    # チェックイン記録を保存
                    with open(CHECKIN_FILE, "a") as f:
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 秒まで
                        f.write(f"{input_id},{name},{comment},{now_str}\n")
                else:
                    st.warning(f"{name} さんはすでにチェックイン済みです。")
            else:
                st.error("未登録のIDです。")
        else:
            st.warning("IDを入力してください。")

    st.markdown("---")
    
    show_checkin_log(CHECKIN_FILE)        
   
    show_not_checked_in_participants(df, CHECKIN_FILE)

   
    st.markdown("---") 
    # --- チェックイン記録から削除する機能 ---
    if os.path.exists(CHECKIN_FILE):
        log_df = pd.read_csv(CHECKIN_FILE)
        if not log_df.empty:
            st.markdown("#### ❌ 間違ったチェックインを削除")
            del_id = st.text_input("削除したい参加者IDを入力してください", key="delete_id")
            if st.button("このIDのチェックイン記録を削除"):
                if del_id and del_id.isdigit():
                    before = len(log_df)
                    log_df = log_df[log_df['ID'] != int(del_id)]
                    after = len(log_df)
                    if before != after:
                        log_df.to_csv(CHECKIN_FILE, index=False)
                        st.success(f"ID {del_id} のチェックイン記録を削除しました。")
                        #st.rerun()
                    else:
                        st.warning(f"ID {del_id} の記録は見つかりませんでした。")
                else:
                    st.warning("正しいIDを入力してください。")
                    
    st.markdown("---")
    
    st.markdown("##### 画面のリロード")
    if st.button("画面をリロード"):
        st.rerun()  # 画面をリロードするボタン
    
    st.markdown("---")
    
    
    # チェックインログのダウンロードボタン
    now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    st.markdown("##### チェックインログをCSV形式でダウンロードできます。")
    st.download_button(
        label=f"{CHECKIN_FILE}をダウンロード",
        data=open(CHECKIN_FILE, "rb").read(),
        file_name=f"{CHECKIN_HEAD}{meeting_type}_{now_str}.csv",
        mime="text/csv"
    )
    
    # --- チェックインCSVの複製＋未チェックインリスト追記 ---
    if os.path.exists(CHECKIN_FILE):
        # チェックインCSVの内容を取得
        with open(CHECKIN_FILE, "r") as f:
            checkin_csv = f.read()
        # 未チェックインIDリストを取得
        registered_ids = set(df['ID'].astype(str).str.strip())
        checked_in_ids = set(pd.read_csv(CHECKIN_FILE, usecols=[0], names=["ID"])['ID'].astype(str).str.strip())
        not_checked_in = registered_ids - checked_in_ids
        not_checked_in_sorted = sorted([int(x) for x in not_checked_in])
        
        # 未チェックイン者のIDと名前を抽出
        not_checked_df = df[df['ID'].isin(not_checked_in_sorted)][['ID', 'Name']]
        # 末尾に追記するテキスト
        append_text = "\n\n未チェックイン者リスト:\n"
        append_text += not_checked_df.to_csv(index=False, header=False)
        # 複製データ
        duplicated_csv = checkin_csv + append_text

        st.download_button(
            label=f"{CHECKIN_FILE}＋未チェックインリストをダウンロード",
            data=duplicated_csv,
            file_name=f"{CHECKIN_HEAD}{meeting_type}_{now_str}_with_not_checked.csv",
            mime="text/csv"
        )
    
    st.markdown("---")
    
    

#%%----
if __name__ == "__main__":
    main()