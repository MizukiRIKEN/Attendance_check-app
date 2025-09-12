MEETING_NAME = "NuSym25"
# ファイルの保存場所
DIR_OUTPUT = 'output'
# 元データのExcelファイル
ORIGINAL_DATABASE = "participant_list_20250902_4.xlsx"
# 元データのシート名
DATABASE_SHEET = "名簿"
# 参加者確認用CSVファイル
PARTICIPANT_LIST = f"{DIR_OUTPUT}/{MEETING_NAME}_participant_list.csv"

# 参加確認のCSVファイル  参加者確認をしたファイルを指定する
CHECKED_LIST = f"{DIR_OUTPUT}/{MEETING_NAME}_participant_checked_list.csv"

REGISTERED_HEAD = MEETING_NAME+"_Regs_"
CHECKIN_HEAD = MEETING_NAME+"_Chkin_"

# Judgment keys for registration and attendance
REGISTRATION_STATUS_KEYS = ['Registration state','Withdrawn']
ATTENDANCE_STATUS_KEYS = 'Attendance state'

# Extract columns for registration and attendance
REGISTRATION_COLUMNS = [
    'ID', 'Name', 'Excursion', 'Banquet', 'Dietary Request', 'Detail of Dietary Request'
]

# checkin用の列
MEETING_TYPES = [
    "Excursion",
    "Going",
    "Ropeway",
    "Banquet"
]

Checking_keys = [
    'Excursion',
    'Banquet',
    'Dietary Request'
]

dtype_dict = {
    'ID': str,
    'Name': str,
    'Entrance': str,
    'Session': str,
    'Excursion': str,
    'Ropeway': str,
    'Banquet': str,
    'Special food': str,
    'Time': str,
    'Comment': str,
    'Receptionist': str
}