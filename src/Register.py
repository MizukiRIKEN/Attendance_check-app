import streamlit as st
from utils import *
from types import *
import pandas as pd
from datetime import datetime
import os
from config import Personal_info
from config import dtype_dict


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
def main():
    st.markdown("# NuSym25 Register application")

    REGISTERED_FILE = "NuSym25_registered.csv"

    if not os.path.exists(REGISTERED_FILE):
        st.error(f"登録者リストファイルが見つかりません: {REGISTERED_FILE}")
        return  

    df = pd.read_csv(REGISTERED_FILE, dtype=dtype_dict)

    st.markdown("### IDを検索するため名前の一部を入力してください")
    input_name = st.text_input("Name")

    # --- セッションでIDを保持 ---
    if "user_index" not in st.session_state:
        st.session_state.user_index = None

    if st.button("検索"):
        if input_name:
            user = df[df['Name'].str.contains(input_name, case=False, na=False)]
            if not user.empty:
                st.write(user)
            else:
                st.warning("未登録の名前です。")
        else:
            st.warning("名前を入力してください。")

    st.markdown("---")

    st.markdown("### 登録者のIDを入力して登録してください")
    input_id = st.text_input("登録するID")

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
            df.to_csv(REGISTERED_FILE, index=False)
            st.rerun()

    # 変更モードの場合のみ modify_register のフォームを表示
    if st.session_state.get("modify_mode", False) and st.session_state.user_index is not None:
        rguser = df.loc[st.session_state.user_index]
        name = rguser['Name']

        st.markdown(f"### {name} さんの登録内容を変更")
        selected_key = st.selectbox("変更したい項目を選択してください", [k for k in Personal_info.keys() if k != 'ID'])

        # 項目ごとに入力欄を表示
        if selected_key in ['session','Banquet', 'Excursion', 'Ropeway', 'Special food']:
            new_value = st.selectbox(f"{selected_key} (現在の値: {rguser[selected_key]})", ['Yes', 'No'], index=0 if rguser[selected_key] == 'Yes' else 1)
        else:
            new_value = st.text_input(f"{selected_key} (現在の値: {rguser[selected_key]})", value=str(rguser[selected_key]))

        if st.button("更新"):
            df.loc[st.session_state.user_index] = new_value
            now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
            df.loc[st.session_state.user_index, 'Time'] = now_str
            df.to_csv(REGISTERED_FILE, index=False)
            st.success(f"{name} さんの登録内容を更新しました。 ✅")
            st.write("変更後の情報:")
            st.write(df.loc[st.session_state.user_index])
            st.session_state.modify_mode = False
            st.session_state.user_index = None
            st.rerun()

    st.write(df)

if __name__ == "__main__":
    main()