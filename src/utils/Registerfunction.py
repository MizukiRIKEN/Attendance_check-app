    
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