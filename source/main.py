from dataclasses import dataclass

from flask import Flask, redirect, url_for, request, render_template
from sqlalchemy import func
from arabic_words_db import ArabicWordsDB, Labels, WordsLabels, Words, Sentences
from includes_utils import get_top_variables, get_trailer_variables


app = Flask(__name__, template_folder="templates", static_folder="static")


def get_label_data_dicts():
    with ArabicWordsDB() as arabic_words_db:
        rows = arabic_words_db.session.query(Labels.ID, Labels.labelName).all()

    label_data_dicts = []
    for label_row in rows:
        label_id = label_row.ID
        label_name = label_row.labelName

        with ArabicWordsDB() as arabic_words_db:
            word_count = arabic_words_db.session.query(func.count(WordsLabels.wordID)). \
                filter(WordsLabels.labelID == label_id).scalar()

            if word_count <= 10:
                tag_size = "0.8em"
            elif 11 <= word_count <= 30:
                tag_size = "1em"
            elif 71 <= word_count <= 120:
                tag_size = "1.5em"
            elif 121 <= word_count <= 180:
                tag_size = "1.7em"
            elif 180 <= word_count <= 300:
                tag_size = "1.9em"
            else:
                tag_size = "2.4em"

        label_data_dict = {}
        label_data_dict["name"] = label_name
        label_data_dict["title"] = f"there are {word_count} words in this topic"
        label_data_dict["href"] = f"label.asp?id={label_id}"
        label_data_dict["style_string"] = f"font-size:{tag_size}"

        label_data_dicts.append(label_data_dict)

    return label_data_dicts


@app.route("/labels.asp")
def labels_handler():
    label_data_dicts = get_label_data_dicts()

    return render_template("labels.html", label_data_dicts=label_data_dicts)


@app.route("/label.asp")
def label_handler():
    label_id = request.args.get("id")
    if not label_id:
        label_id = "no label_id was found"

    with ArabicWordsDB() as arabic_words_db:
        row = arabic_words_db.session.query(Labels.labelName).filter(Labels.ID == label_id).one()

    label_name = row.labelName

    with ArabicWordsDB() as arabic_words_db:
        rows = arabic_words_db.session.query(WordsLabels.wordID).filter(WordsLabels.labelID == label_id).all()

    all_label_word_ids = [row.wordID for row in rows]


    with ArabicWordsDB() as arabic_words_db:
        words = arabic_words_db.session.\
            query(Words.id, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
                  Words.pronunciation).filter(Words.id.in_(all_label_word_ids)).all()

    word_count = len(rows)

    label_data_dicts = get_label_data_dicts()

    return render_template("label.html", label_data_dicts=label_data_dicts, label_name=label_name,
                           word_count=word_count, words=words)


@app.route("/sentences.asp")
def sentences_handler():
    with ArabicWordsDB() as arabic_words_db:
        sentence_count = arabic_words_db.session.query(func.count(Sentences.id)).scalar()

    #new query
    with ArabicWordsDB() as arabic_words_db:
        sentences = arabic_words_db.session.query(Sentences).all()

    return render_template("sentences.html", sentence_count=sentence_count, sentences=sentences)

@app.route("/guide.asp")
def guide_handler():
    return render_template("guide.html")


@dataclass
class Image:
    arabic: str
    arabicWord: str

@app.route("/about.asp")
def about_handler():
    return render_template("about.html")

@app.route("/games.mem.asp")
def games_mem_handler():

    image1 = Image("cat", "biss")
    image2 = Image("school", "madrasa")

    images = [image1, image2]
    return render_template("games.mem.html", images=images)


@app.route("/")
def root_handler():
    label_data_dicts = get_label_data_dicts()

    search_string = request.args.get("searchString", "")
    search_string = search_string.strip()

    if search_string.isalpha():  # TODO
        is_search_string_valid = True

        with ArabicWordsDB() as arabic_words_db:
            words = arabic_words_db.session. \
                query(Words.id, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
                      Words.pronunciation).filter(Words.hebrewClean == search_string).all()

    else:
        is_search_string_valid = False
        words = []

    return render_template("default.html", label_data_dicts=label_data_dicts,
                           is_search_string_valid=is_search_string_valid, words=words)







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
