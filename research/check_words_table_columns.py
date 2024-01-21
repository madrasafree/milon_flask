import pyodbc

from arabic_words_db import Words, ArabicWordsDB

query = """SELECT column_name
  FROM information_schema.columns
 WHERE table_schema = 'public'
   AND table_name   = 'words'
     ;"""

column_names_from_postgres = []
with ArabicWordsDB() as arabic_words_db:
    result = arabic_words_db.engine.execute(query)
for column_name in result:
    column_names_from_postgres.append(column_name[0])

#print(column_names_from_postgres)
current_dir =  os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")
db_file_path = Path(parent_dir + "\\database\\arabicWords.mdb")

#connecting to access to extract the column names
MDB = str(db_file_path)
DRV = 'Microsoft Access Driver (*.mdb, *.accdb)'
PWD = ''

con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
cur = con.cursor()

SQL = 'SELECT * FROM words;'
cursor = cur.execute(SQL)

column_names_from_access = [column[0] for column in cursor.description]
#print(column_names_from_access)

column_names_from_postgres_set = set(column_names_from_postgres)
column_names_from_access_set = set(column_names_from_access)

print(column_names_from_access_set - column_names_from_postgres_set)
print(column_names_from_postgres_set - column_names_from_access_set)

