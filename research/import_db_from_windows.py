import csv, pyodbc

from tqdm import tqdm

from arabic_words_db import ArabicWordsDB, History, Labels, Lists, ListsUsers, Log, Media, Sentences, Words, \
    WordsLabels, WordsLists, WordsMedia, WordsRelations, WordsSentences, WordsShort

# set up some constants
#MDB = 'c:/path/to/my.mdb'
#Microsoft Access Driver (*.mdb, *.accdb)

MDB = 'c:/Users/rinat/Desktop/Madrasa/arabicWords.mdb'
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
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()

    SQL = f'SELECT * FROM {table_names};'
    rows = cur.execute(SQL).fetchall()

    class_name = table_name_to_class_name[table_name]

    cur.close()
    con.close()
    for pyodbc_row in tqdm(rows):

        row = class_name(**pyodbc_row)
        try:
            with ArabicWordsDB() as arabic_words_db:
                arabic_words_db.session.merge(row)
        except Exception as exception:
            print(exception, row)
