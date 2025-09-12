import streamlit as st
from utils import *  # ユーティリティ関数をインポート
from types import *  # 型定義をインポート
import pandas as pd
from datetime import datetime
import os
from config import * 

#%%----  
def diffrentiate_checkin(cid, CHECKIN_FILE):
    """
    チェックインの差分を表示する関数
    """
    log_df = pd.read_csv(CHECKIN_FILE)
    fuser = log_df[log_df['ID'] == int(cid)]
    if fuser.empty:
        return True
    else:
        #name = fuser.iloc[0]['Name'] if 'Name' in fuser.columns and not fuser.empty else ""
        #st.error(f"ID {cid}（{name}）はすでにチェックイン済みです。")
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
    
    st.markdown(f"#### {len(checked_in_ids)-1} 人　/　{len(registered_ids)}人中　チェックイン済み")
    
    
    if not not_checked_in:
        st.info("全ての参加者がチェックイン済みです。")
    else:
        st.markdown("##### 未チェックインの参加者ID:")
        st.markdown(f"##### 残り {len(not_checked_in)} 人")
        st.write(f" {not_checked_in_sorted}")

    cf = pd.read_csv(CHECKIN_FILE)
    registerer_counts = cf["Registerer"].value_counts()
    st.write("受付者毎の人数:")
    st.write(registerer_counts)
    
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
    st.title(f"{MEETING_NAME}")
    st.title("✅ 出席確認アプリ")

    REGISTERER = None
    input_registerer = st.text_input("受付者の名前を入力してください。")
    if input_registerer:
        REGISTERER = input_registerer

    if not REGISTERER:
        st.warning("受付者の名前を入力してください。")
        return

    meeting_type = st.selectbox(
        "リストの種類を選択してください",
        options=MEETING_TYPES,
        index=0  # デフォルトで最初のオプションを選択
    )

    REGISTERED_FILE = f"{DIR_OUTPUT}/{REGISTERED_HEAD}{meeting_type}.csv"
    CHECKIN_FILE = f"{DIR_OUTPUT}/{CHECKIN_HEAD}{meeting_type}.csv"

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
        #st.warning(f"チェックイン記録ファイルが見つかりません: {CHECKIN_FILE}")
        st.markdown("#### 新しいチェックインを開始します。-->> ")
        with open(CHECKIN_FILE, "w") as f:
            f.write("ID,Name,Comment,Time,Registerer\n")


    st.markdown(f'<span style="color:blue"> 登録者リストファイル: [{REGISTERED_FILE}]</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="color:blue"> チェックイン記録ファイル: [{CHECKIN_FILE}]</span>', unsafe_allow_html=True)
    st.markdown("---")


    # 入力フォーム
    st.markdown("### 🟢 登録する参加者のIDを入力してください")
    input_id = st.text_input("参加者IDを入力してください", value="", key="ID")

    if input_id:
        user = df[df['ID'] == int(input_id)]
        name = user.iloc[0]['Name'] if not user.empty else None
        if name:
        
            if diffrentiate_checkin(input_id,CHECKIN_FILE):
            
                st.success(f"参加者: [{input_id}] {name} さんを登録しますか？　✅")
                
                comment = st.text_input("コメント（任意）", key="Comment", value="")  # ← コメント欄を追加
                
                if meeting_type == "Banquet":
                    special_request = user.iloc[0]['Dietary Request'] if 'Dietary Request' in user.columns else ""
                    if special_request == 'Yes':
                        st.warning("この参加者は特別食をリクエストしています。")
                st.session_state['regist']= True    
            else:
                st.warning(f"{name} さんはすでにチェックイン済みです。") 
                st.session_state['regist']= False
        else:         
            st.error("未登録のIDです。")
            st.session_state['regist']= False

    
    if st.session_state.get('regist') is True:
        if st.button("登録"):
            # チェックイン記録を保存
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 秒まで
            with open(CHECKIN_FILE, "a") as f:
                f.write(f"{input_id},{name},{comment},{now_str},{REGISTERER}\n")
            st.session_state['regist']= False
            st.session_state['reset']= True
            st.rerun()

    st.markdown("---")
   
    show_not_checked_in_participants(df, CHECKIN_FILE)

    show_checkin_log(CHECKIN_FILE)

    st.markdown("---")
    # --- チェックイン記録から削除する機能 ---
    if os.path.exists(CHECKIN_FILE):
        log_df = pd.read_csv(CHECKIN_FILE)
        if not log_df.empty:
            st.markdown("#### ❌ 間違ったチェックインを削除")
            del_id = st.text_input("削除したい参加者IDを入力してください", key="delete_id")
            user = log_df[log_df['ID'] == int(del_id)] if del_id and del_id.isdigit() else pd.DataFrame()
            name = user.iloc[0]['Name'] if not user.empty else ""
            if not del_id or name!="":
                st.write(f"削除対象: ID {del_id} {name} さん")
                if st.button("チェックイン記録を削除"):
                    if del_id and del_id.isdigit():
                        before = len(log_df)
                        log_df = log_df[log_df['ID'] != int(del_id)]
                        after = len(log_df)
                    if before != after:
                        log_df.to_csv(CHECKIN_FILE, index=False)
                        st.success(f"ID {del_id}:{name}のチェックイン記録を削除しました。")
                        #st.rerun()
            elif del_id and del_id.isdigit() and user.empty:
                st.warning(f"ID {del_id} の記録は見つかりませんでした。")
                    
    st.markdown("---")

    st.markdown("### ️🟢 登録する参加者の氏名の一部を入力してください")
    input_name = st.text_input("Name", key="Name")

    if input_name: 
        user = df[df['Name'].str.contains(input_name, case=False, na=False)]
        if not user.empty:
            st.dataframe(
                user,
                use_container_width=True,
                hide_index=True,
                column_config={"ID":st.column_config.Column("ID", disabled=True, required=True, width="small", pinned=True),
                               "Name": "氏名"}
            )
            #st.write(user)
            # ユーザー選択用のセレクトボックスを追加
            user_options = [f"{row['ID']} : {row['Name']}" for _, row in user.iterrows()]
            selected_user = st.selectbox("リストから参加者を選択してください", user_options)
            if selected_user:
                SELECTED_ID = selected_user.split(" : ")[0]  # IDのみ抽出
        else:
            st.warning("未登録の名前です。")

    st.markdown("##### 画面の更新")
    if st.button("画面の更新"):
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

if st.session_state.get("reset") is True:
    st.session_state['ID'] = ""
    st.session_state['Comment']=""
    st.session_state['reset'] = False

#%%----
if __name__ == "__main__":
    main()