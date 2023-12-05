import os
from pathlib import Path
import pyodbc
from tqdm import tqdm
from source.arabic_words_db import (ArabicWordsDB, History, Labels, Lists,
                                    ListsUsers, Log, Media, Sentences, Words,
                                    WordsLabels, WordsLists, WordsMedia,
                                    WordsRelations, WordsSentences, WordsShort)

# set up some constants
current_dir =  os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")
db_file_path = Path(parent_dir + "\\database\\arabicWords.mdb")
MDB = str(db_file_path)
DRV = 'Microsoft Access Driver (*.mdb, *.accdb)'
PWD = ''

table_name_to_class_name = {
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


table_names = "history labels lists listsUsers log media sentences words wordsLabels wordsLists wordsMedia " \
              "wordsRelations wordsSentences wordsShort".split()


for table_name in table_names:
    print(table_name)
    if table_name != "words":
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
            with ArabicWordsDB() as arabic_words_db:
                print(row)
                arabic_words_db.session.merge(row)
        except Exception as exception:
            print(row)
            print(exception)
            break
