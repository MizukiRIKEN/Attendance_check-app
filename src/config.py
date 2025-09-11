# 会議名
MEETING_NAME = "NuSym25"
DIR_OUTPUT = 'output'
PARTICIPANT_LIST = f"{DIR_OUTPUT}/{MEETING_NAME}_participant_list.csv"
REGISTERED_HEAD = MEETING_NAME+"_Regs_fin_"
CHECKIN_HEAD = MEETING_NAME+"_Chkin_fin_"


#リストを選択する
MEETING_TYPES = [
    "Excursion",
    "Ropeway",
    "Going",
    "Return",
    "Banquet"
]

Personal_info = {
    'ID': ' ',
    'Name': ' ',
    'Entrance': ' ',
    'Session': ' ',
    'Excursion': ' ',
    'Dietary Request': ' ',
    'Detail of Dietary Request': ' ',
    'Ropeway': ' ',
    'Banquet': ' ',
    'Time': ' ',
    'Comment': ' ',
    'Receptionist': ' '
}

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