# 会議名
MEETING_NAME = "NuSym25"
REGISTERED_FILE = f"{MEETING_NAME}_registered.csv"

#リストを選択する
MEETING_TYPES = [
    "Session",
    "Banquet",
    "Excursion",
    "Ropeway",
    "Going",
    "Return"
]

 
REGISTERED_HEAD = "Registered_"
CHECKIN_HEAD = "Checkin_"
   



Personal_info = {
    'ID': '',
    'Name': '',
    'Session': '',
    'Banquet': '',
    'Excursion': '',
    'Ropeway': '',
    'Special food': '',
    'Time': '',
    'Comment': '',
    'Registerer': ''
}

dtype_dict = {
    'ID': str,
    'Name': str,
    'Session': str,
    'Banquet': str,
    'Excursion': str,
    'Ropeway': str,
    'Special food': str,
    'Time': str,
    'Comment': str,
    'Registerer': str  
}