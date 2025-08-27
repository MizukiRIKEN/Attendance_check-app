import streamlit as st
from utils import *
from types import *
import pandas as pd
from datetime import datetime
import os
from config import Personal_info
from config import dtype_dict
from config import MEETING_NAME, REGISTERED_FILE

#%%
def check_register(df, user_idx):
    if user_idx is None or user_idx < 0 or user_idx >= len(df):
        return False
    
    rguser = df.loc[user_idx]
    if not rguser.empty:
        name = rguser['Name']
        #st.write(rguser)
        st.write(rguser)

        stamp = df.loc[user_idx, 'Time']   
        if stamp is None or pd.isna(stamp):                        
            st.success(f"{name} さんは未登録です。")
            return True
        else:
            st.warning(f"{name} さんはすでに登録済みです。")
            return False
    return False


#%%
def modify_register(df, user_idx):
    rguser = df.loc[user_idx]
    name = rguser['Name']
    
    if st.selectbox("変更したい項目を選択してください", list(Personal_info.keys())) == 'ID':
        st.warning("IDは変更できません。")
    else:
        for key in Personal_info.keys():
            if key == 'Banquet':
                new_value = st.selectbox(f"{key} (現在の値: {rguser[key]})", value=['Yes', 'No'], index=0 if rguser[key] == 'Yes' else 1)
                df.loc[user_idx, key] = new_value
            elif key == 'Excursion':
                new_value = st.selectbox(f"{key} (現在の値: {rguser[key]})", value=['Yes', 'No'], index=0 if rguser[key] == 'Yes' else 1)
                df.loc[user_idx, key] = new_value
                df.loc[user_idx, 'Ropeway'] = new_value

        df.to_csv(REGISTERED_FILE, index=False)
        st.write(df.loc[user_idx])
        st.success(f"{name} さんの出席を更新して登録しました。 ✅")
        st.write("変更後の情報:")
        st.write(df.loc[user_idx])

#%%
def get_Last_Registered_User(df):
    if df.empty:
        return None
    return int(df.loc[df.index[-1], 'ID'])
    
#%%
def main():
    st.markdown(f"# {MEETING_NAME} Registration")

    REGISTERERER = None
    input_registerer = st.text_input("受付者の名前を入力してください。")
    if input_registerer:
        REGISTERERER = input_registerer

    if not REGISTERERER:
        st.warning("受付者の名前を入力してください。")
        return
    
    if not os.path.exists(REGISTERED_FILE):
        st.error(f"登録者リストファイルが見つかりません: {REGISTERED_FILE}")
        return  

    df = pd.read_csv(REGISTERED_FILE, dtype=dtype_dict)

    st.markdown("### ️🟢 登録する氏名の一部を入力してください")
    input_name = st.text_input("Name")
    selected_id = None  # 追加

    if input_name: 
        user = df[df['Name'].str.contains(input_name, case=False, na=False)]
        if not user.empty:
            st.write(user)
            # ユーザー選択用のセレクトボックスを追加
            user_options = [f"{row['ID']} : {row['Name']}" for _, row in user.iterrows()]
            selected_user = st.selectbox("リストから参加者を選択してください", user_options)
            if selected_user:
                selected_id = selected_user.split(" : ")[0]  # IDのみ抽出
        else:
            st.warning("未登録の名前です。")
            st.markdown("##### 新規登録しますか？")
            input_new_name = st.text_input("新規登録する氏名を入力してください", value=input_name)
            if st.button("新規登録"):
                new_id = get_Last_Registered_User(df) + 1 if get_Last_Registered_User(df) is not None else 1
                new_user = {
                    'ID': int(new_id),
                    'Name': input_new_name,
                    'Session': 'Yes',
                    'Banquet': 'Yes',
                    'Excursion': 'Yes',
                    'Ropeway': 'Yes',
                    'Special food': 'No',
                    'Time': datetime.now().strftime("%Y%m%d-%H%M%S"),
                    'Comment': '',
                    'Registerer': REGISTERERER
                }
                df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
                df.to_csv(REGISTERED_FILE, index=False)
                st.success(f"{input_new_name} さんを新規登録しました。 ✅")
                st.write("登録後の情報:")
                st.write(df.loc[df['Name'] == input_new_name])
                st.session_state.user_index = None
                st.session_state.modify_mode = False
                st.rerun()

    # --- セッションでIDを保持 ---
    if "user_index" not in st.session_state:
        st.session_state.user_index = None

    st.markdown("---")
    st.markdown("### 🟢 登録者のIDを入力して登録してください")
    # 選択されたIDがあれば自動入力
    input_id = st.text_input("登録するID", value=selected_id if selected_id else "")

    st.markdown(f"--- 現在の時刻: {datetime.now().strftime('%Y%m%d-%H%M%S')} ---")

    if st.button("登録"):
        if input_id and input_id.isdigit() and int(input_id) > 0:
            user_idx = df.index[df['ID'] == input_id]
            st.session_state.user_index = user_idx[0] if not user_idx.empty else None
        else:
            st.warning("正しいIDを入力してください。")



    if check_register(df, st.session_state.user_index):
        st.markdown("#### 登録を選択してください")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("変更せず登録する"):
                now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
                st.write(f"{df.loc[st.session_state.user_index]['Name']} さんの登録を変更せずに保存します")
                df.loc[st.session_state.user_index, 'Time'] = now_str
                df.loc[st.session_state.user_index, 'Registerer'] = REGISTERERER
                df.to_csv(REGISTERED_FILE, index=False)
                st.success(f"{input_id} を登録しました。 ✅")
                st.write("登録後の情報:")
                st.write(df.loc[st.session_state.user_index])
                st.session_state.user_index = None
                st.session_state.modify_mode = False
                st.rerun()
        with col2:
            if st.button("変更して登録する"):
                st.session_state.modify_mode = True  # ← 変更モードに切り替え
                st.rerun()

    elif st.session_state.user_index is not None:
        if st.button("登録を修正"):
            df.loc[st.session_state.user_index, 'Time'] = None
            df.loc[st.session_state.user_index, 'Registerer'] = REGISTERERER
            df.to_csv(REGISTERED_FILE, index=False)
            st.rerun()

    # 変更モードの場合のみ modify_register のフォームを表示
    if st.session_state.get("modify_mode", False) and st.session_state.user_index is not None:
        rguser = df.loc[st.session_state.user_index]
        name = rguser['Name']

        st.markdown(f"### {name} さんの登録内容を変更")
        selected_key = st.selectbox("変更したい項目を選択してください", [k for k in Personal_info.keys() if k != 'ID'])

        try:
        # 項目ごとに入力欄を表示
            if selected_key in ['Session','Banquet', 'Excursion', 'Ropeway', 'Special food']:
                options = ['Yes', 'No']
                current_value = str(rguser[selected_key])
                if current_value in options:
                    default_index = options.index(current_value)
                else:
                    default_index = 0  # デフォルトは 'Yes'

                new_value = st.selectbox(
                    f"{selected_key} (現在の値: {current_value})",
                    options,
                    index=default_index
                )
            elif selected_key != 'Registerer':
                new_value = st.text_input(f"{selected_key} (現在の値: {rguser[selected_key]})", value=str(rguser[selected_key]))
            update = st.button("更新", key="update_button")
            if update and new_value:
                df.loc[st.session_state.user_index, selected_key] = new_value
                df.loc[st.session_state.user_index, 'Registerer'] = REGISTERERER
                df.to_csv(REGISTERED_FILE, index=False)
                st.success(f"{name} さんの登録内容を更新しました。 ✅")
                st.write("変更後の情報:")
                st.write(df.loc[st.session_state.user_index])
        except KeyError:
            st.error("無効なキーです。")

        if st.button("保存して終了"):
            now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
            df.loc[st.session_state.user_index, 'Time'] = now_str
            df.loc[st.session_state.user_index, 'Registerer'] = REGISTERERER
            df.to_csv(REGISTERED_FILE, index=False)
            st.session_state.modify_mode = False
            st.session_state.user_index = None
            st.rerun()

    st.markdown("---")
    
    if st.button("画面の更新"):
        st.rerun()  # 画面をリロードするボタン
        
    st.markdown("#### Status ")
    st.dataframe(
        df,
        hide_index=True,
        column_config={
            "ID": st.column_config.Column("ID", disabled=True, required=True, width="small", pinned=True)
        }
    )

if __name__ == "__main__":
    main()