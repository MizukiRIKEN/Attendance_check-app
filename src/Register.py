import streamlit as st
from utils import *  # ユーティリティ関数をインポート
from types import *  # 型定義をインポート
import pandas as pd
from datetime import datetime
import os
from config import Personal_info
from config import dtype_dict

#%%
def main():
    st.markdown("# NuSym25 Register application")

    REGISTERED_FILE = "NuSym25_registered.csv"

    if not os.path.exists(REGISTERED_FILE):
        st.error(f"登録者リストファイルが見つかりません: {REGISTERED_FILE}")
        return  
    
    # CSVを読み込む
    df = pd.read_csv(REGISTERED_FILE, dtype=dtype_dict)
    # 出席者リストを表示
    st.markdown("### IDを検索するため名前の一部を入力してください")
    input_name = st.text_input("Name")
    
    
    if st.button("検索"):
        if input_name:
            # 部分一致で名前を抽出
            user = df[df['Name'].str.contains(input_name, case=False, na=False)]
            if not user.empty:
                #for idx, row in user.iterrows():
                #    st.write(f"参加者: [{row['ID']}] {row['Name']} さん")
                st.write(user)
            else:
                st.warning("未登録の名前です。")
        else:
            st.warning("名前を入力してください。")

    st.markdown("---")

    st.markdown("### 登録者のIDを入力して登録してください")
    input_id = st.text_input("登録するID")
    
    now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    st.markdown(f"--- 現在の時刻: {now_str} ---")
    
    if st.button("登録"):
        if input_id:
            user_idx = df.index[df['ID'] == int(input_id)]
            if not user_idx.empty:
                rguser = df.loc[user_idx[0]]
                if not rguser.empty:
                    name = rguser['Name']
                    #st.write(rguser)
                    st.write(f" 参加者: [{input_id}] {name} さんが見つかりました。")
                    st.write(df.loc[user_idx])

                    stamp = df.loc[user_idx[0], 'Time']   

                    if stamp is None or pd.isna(stamp):                        
                        st.success(f"{name} さんは未登録です。")

                        # 出席時間を登録
                        update = st.toggle("変更せず登録する", value=True)
                        if update:
                            df.loc[user_idx[0], 'Time'] = now_str
                                                
                        else:
                            if st.selectbox("変更したい項目を選択してください", list(Personal_info.keys())) == 'ID':
                                st.warning("IDは変更できません。")
                                return
                            else:
                                for key in Personal_info.keys():
                                    if key == 'Banquet':
                                        new_value = st.selectbox(f"{key} (現在の値: {rguser[key]})", value=['Yes', 'No'], index=0 if rguser[key] == 'Yes' else 1)
                                        df.loc[user_idx[0], key] = new_value
                                    elif key == 'Excursion':
                                        new_value = st.selectbox(f"{key} (現在の値: {rguser[key]})", value=['Yes', 'No'], index=0 if rguser[key] == 'Yes' else 1)
                                        df.loc[user_idx[0], key] = new_value
                                        df.loc[user_idx[0], 'Ropeway'] = new_value
                                
                                st.write("変更後の情報:")
                                st.write(df.loc[user_idx])
                        
                        df.to_csv(REGISTERED_FILE, index=False)
                        st.write(df.loc[user_idx])
                        st.success(f"{name} さんの出席を登録します ✅")
                    else:
                        st.warning(f"{name} さんはすでに登録済みです。")
            else:
                new_entry = Personal_info.copy()
                new_entry['ID'] = pd.max(df['ID']) + 1 if not df.empty else 1
                new_entry['Time'] = now_str
                new_entry['Name'] = input_name if input_name else "Unknown"
                new_entry['Session'] = 'No'
                new_entry['Banquet'] = 'No'
                new_entry['Excursion'] = 'No'
                new_entry['Ropeway'] = 'No'
                new_entry['Special food'] = 'No'
                new_entry['Comment'] = ''
                new_entry = pd.Series(new_entry)
                st.write(f"新規登録: {new_entry['ID']} - {new_entry['Name']}")
                st.write("新規登録の情報:")
                st.write(new_entry)
                #df = df.append(new_entry, ignore_index=True)
                #df.to_csv(REGISTERED_FILE, index=False)
                #st.success(f"ID {input_id} を登録しました。")
        else:
            st.warning("登録するIDを入力してください。")
            




    # 出席者リストを表示
    st.write(df)


#%%----
if __name__ == "__main__":
    main()