import streamlit as st
from utils import *  # ユーティリティ関数をインポート
from types import *  # 型定義をインポート
import pandas as pd
from datetime import datetime
import os
from config import MEETING_TYPES

#%%
def main():
    st.markdown("# NuSym25 Register application")

    REGISTERED_FILE = "NuSym25_registered.csv"

    if not os.path.exists(REGISTERED_FILE):
        st.error(f"登録者リストファイルが見つかりません: {REGISTERED_FILE}")
        return  
    
    # CSVを読み込む
    df = pd.read_csv(REGISTERED_FILE, dtype={'ID': str, 'Name': str, 'Session': str, 'Banquet': str, 'Excursion': str, 'Ropeway': str, 'Special food': str, 'Time': str, 'Comment': str})
    # 出席者リストを表示
    st.markdown("### IDを入力してください")
    input_id = st.text_input("ID")
    st.markdown("### または、名前を入力してください")
    input_name = st.text_input("Name")
    
    if st.button("検索"):
        if input_id:
            user = df[df['ID'] == int(input_id)]
            if not user.empty:
                name = user.iloc[0]['Name']
                st.write(f"参加者: [{input_id}] {name} さん")
                st.write(user)
            else:
                st.warning("未登録のIDです。")

        elif input_name:
            # 部分一致で名前を抽出
            user = df[df['Name'].str.contains(input_name, case=False, na=False)]
            if not user.empty:
                #for idx, row in user.iterrows():
                #    st.write(f"参加者: [{row['ID']}] {row['Name']} さん")
                st.write(user)
            else:
                st.warning("未登録の名前です。")
        else:
            st.warning("IDまたは名前を入力してください。")


    st.markdown("### 登録者のIDを入力して登録してください")
    input_id = st.text_input("登録するID")
    
    now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    if st.button("登録"):
        if input_id:
            user_idx = df.index[df['ID'] == int(input_id)]
            if not user_idx.empty:
                rguser = df.loc[user_idx[0]]
            if not rguser.empty:
                name = rguser['Name']
                st.write(rguser)
                st.write(f" 参加者: [{input_id}] {name} さん")
                
                stamp = df.loc[user_idx[0], 'Time']   

                if not stamp:
                    df.loc[user_idx[0], 'Time'] = now_str
                    df.to_csv(REGISTERED_FILE, index=False)
                    st.write(df.loc[user_idx])
                    st.success(f"{name} さんの出席を登録します ✅")
                    # チェックイン記録を保存
                else:
                    st.warning(f"{name} さんはすでに登録済みです。")
                    
            else:
                new_entry = {'ID': input_id, 'Name': '', 'Excursion': None}
                df = df.append(new_entry, ignore_index=True)
                df.to_csv(REGISTERED_FILE, index=False)
                st.success(f"ID {input_id} を登録しました。")
        else:
            st.warning("登録するIDを入力してください。")
            




    # 出席者リストを表示
    st.write(df)


#%%----
if __name__ == "__main__":
    main()