import csv, pyodbc

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



# connect to db
con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
cur = con.cursor()

# run a query and get the results
SQL = 'SELECT * FROM words;' # your query goes here
rows = cur.execute(SQL).fetchall()

cur.close()
con.close()
for row in rows:
    print(row)
    break
