from tqdm import tqdm
from pathlib import Path
import pyodbc
import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from arabic_words_db import (ArabicWordsDB, History, Labels, Lists,
                                    ListsUsers, Log, Media, Sentences, Words,
                                    WordsLabels, WordsLists, WordsMedia,
                                    WordsRelations, WordsSentences, WordsShort)
from arabic_users_db import (ArabicUsersDB, AllowEdit, Log, LoginLog, Users, UsersWordsFollow)

 
current_dir =  os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")
root_dir = os.path.abspath(current_dir + "/../../")

# Constant variable
table_name_to_class_name_arabicWords = {
    "history": History,
    "labels": Labels,
    "lists": Lists,
    "listsUsers": ListsUsers,
    "log": Log,
    "media": Media,
    "sentences": Sentences,
    "words": Words,
    "wordsLabels": WordsLabels,
    "wordsLists": WordsLists,
    "wordsMedia": WordsMedia,
    "wordsRelations": WordsRelations,
    "wordsSentences": WordsSentences,
    "wordsShort": WordsShort
}

table_name_to_class_name_arabicUsers = {
    "allowEdit": AllowEdit, 
    "log":Log, 
    "loginLog": LoginLog, 
    "users": Users, 
    "usersWordsFollow": UsersWordsFollow
}

table_names_arabicWords = "history labels lists listsUsers log media sentences words wordsLabels wordsLists wordsMedia " \
              "wordsRelations wordsSentences wordsShort".split()
table_names_arabicUsers = "allowEdit log loginLog users usersWordsFollow".split()

columns_to_load_filter_arabicWords = ["wordsRelations"] #"wordsLists" #"words", "wordsMedia", "media", "wordsLabels", "labels"]
columns_to_load_filter_arabicUsers = ["users"]


db_file_path_arabicWords = Path(root_dir + "\\database\\arabicWords.mdb")
db_file_path_arabicUsers = Path(root_dir + "\\database\\arabicUsers.mdb")

database_arabicWords = ArabicWordsDB()
database_arabicUsers = ArabicUsersDB()

# Editable Variables
table_name_to_class_name = table_name_to_class_name_arabicWords
table_names = table_names_arabicWords
columns_to_load_filter = columns_to_load_filter_arabicWords
db_file_path = db_file_path_arabicWords
database = database_arabicWords

# Generic Import Algorithm
MDB = str(db_file_path)
DRV = 'Microsoft Access Driver (*.mdb, *.accdb)'
PWD = ''

for table_name in table_names:
    print(table_name)
    if (table_name not in columns_to_load_filter):
        continue
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    
    SQL = f'SELECT * FROM {table_name};'
    cursor = cur.execute(SQL)

    columns = [column[0] for column in cursor.description]
    print(len(columns))
    rows = cursor.fetchall()

    class_name = table_name_to_class_name[table_name]

    cur.close()
    con.close()

    for pyodbc_row in tqdm(rows):
        row_dict = {}
        for x, y in zip(columns, pyodbc_row):
            row_dict[x] = str(y)

        row = class_name(**row_dict)
        try:
            with database as db:
                print(row)
                db.session.merge(row)
        except Exception as exception:
            print(row)
            print(exception)
            break
