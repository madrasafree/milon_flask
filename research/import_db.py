from pathlib import Path
from meza import io
from arabic_words_db import ArabicWordsDB, History, Labels, Lists, ListsUsers, Log, Media, Sentences, Words, \
    WordsLabels, WordsLists, WordsMedia, WordsRelations, WordsSentences, WordsShort
from tqdm import tqdm


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


db_file_path = Path("~/arabicWords.mdb").expanduser()
db_file_path_string = str(db_file_path)


#  mdb-tables arabicWords.mdb

table_names = "history labels lists listsUsers log media sentences words wordsLabels wordsLists wordsMedia " \
              "wordsRelations wordsSentences wordsShort".split()


# dbSession = psycopg2.connect("dbname=arabicWords")
#
# dbCursor = dbSession.cursor()



for table_name in table_names:
    print(table_name)
    if table_name == "words":
        continue


    rows = io.read_mdb(db_file_path_string, table=table_name)
    class_name = table_name_to_class_name[table_name]
    for row in tqdm(rows):
        # values_list = list(row.values())
        # print(values_list)
        row = class_name(**row)

        try:
            with ArabicWordsDB() as arabic_words_db:
                arabic_words_db.session.merge(row)
        except Exception as exception:
            print(exception, row)

        # match table_name:
        #     case "history":
        #         pass
        #     case "labels":
        #        pass
        #     case "wordsLabels":
        #        wordID, labelID
        #     case _:
        #         pass



    tables_lines = []
    for row in rows:
        line = "\t".join(row.values())
        tables_lines.append(line)

    table_file_path = Path(f"~/{table_name}.tsv").expanduser()
    file_text = "\n".join(tables_lines)
    table_file_path.write_text(file_text)





    # tables_lines = []
    # for row in rows:
    #     line = "\t".join(row.values())
    #     tables_lines.append(line)
    #
    # table_file_path = Path(f"~/{table_name}.tsv").expanduser()
    # file_text = "\n".join(tables_lines)
    # table_file_path.write_text(file_text)


        # row_values_tuple_string = str(tuple(row_values))
        # row_values_tuple_string = row_values_tuple_string
        # sqlInsertRow = f"INSERT INTO {table_name} VALUES{row_values_tuple_string}"
        # print(sqlInsertRow)
        # result = dbCursor.execute(sqlInsertRow)
        # dbSession.commit()
        # print(result)


        # exit()
        # print(f"create table {table_name}")
        # print("(")
        # first_row = next(rows)
        # for field_name in first_row.keys():
        #     print(f"\t{field_name} text,")
        # print(");")
        # print()
        #




#
#
# for table_name in table_names:
#     rows = io.read_mdb(db_file_path_string, table=table_name)
#     print(f"create table {table_name}")
#     print("(")
#     first_row = next(rows)
#     for field_name in first_row.keys():
#         print(f"\t{field_name} text,")
#     print(");")
#     print()
#
