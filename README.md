# Attendance_check-app
## 会議の参加者登録をするためのアプリです。
## How To Use
### 準備
 python をインストールする。
 
 (python) pip install pandas 
 
 pip install streamlit

### ファイル名を編集する
src/config.py

###　参加登録をするためのデータベースを作るコード

python src/Extract_csv.py　１

 ORIGINAL_DATABASE  : HP上でレジストレーションしたエクセルファイル

 DATABASE_SHEET    ；参加者情報のリストシート名
 
 PARTICIPANT_LIST　： DATABASE_SHEET から　参加する人だけを抜き出したcsvファイル
 
   REGISTRATION_STATUS_KEYS = ['Registration state','Withdrawn']　参加者を抜き出すための欄とKey

### 参加登録のためのアプリ
streamlit run src/Registraion.py　

 CHECKED_LIST　　　 ：参加確認の情報を保存するファイル。 PARTICIPANT_LISTから作成する。

### 参加登録した　CHEKCED_LIST から　MEETING_TYPES毎の参加者を抜き出す。
src/config.py

#### checkin用のパラメータ
MEETING_TYPES = [
    "Excursion",
    "Going",
    "Ropeway",
    "Banquet"
]

python src/Extract_csv.py 1


 
 
 
