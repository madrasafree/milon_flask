from dataclasses import dataclass
from sound_index_function import get_sound_index, get_clean_word
from flask import Flask, redirect, url_for, request, render_template
from sqlalchemy import func, and_, or_, not_
from arabic_words_db import ArabicWordsDB, Labels, WordsLabels, Words, WordsShort, Sentences, WordsMedia
from includes_utils import get_top_variables, get_trailer_variables
from config.config import config

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

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

    # INITIALIZE VARIABLES
    is_search_string_valid = True
    label_data_dicts = []
    cleaned_word = ""
    sound_index = ""
    exact_match_words = []
    sound_like_words = []
    letter_like_words = []
    search_words = []
    short_words = []

    label_data_dicts = get_label_data_dicts()
    search_string = request.args.get("searchString", "")
    search_string_strip = search_string.strip()
    cleaned_word = get_clean_word(search_string_strip)

    #DEBUG
    print("search_string = " + search_string)
    print("search_string_strip = " + search_string_strip)
    print("cleaned_word = " + cleaned_word)
    
    invalid_word_filter = and_(
        Words.show == "True",
        Words.hebrewTranslation != "None",
        Words.arabic != "None",
        Words.arabicWord != "None"
    )

    if len(cleaned_word)>0:
        if (len(cleaned_word)>1):
            # CASE 1: "Identical": Words exactly as searched
            with ArabicWordsDB() as arabic_words_db:
                exact_match_words = arabic_words_db.session. \
                    query(Words.id, Words.show, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
                        Words.pronunciation).filter(and_(invalid_word_filter,       # TODO: FIX!
                                                        Words.hebrewTranslation.contains(search_string_strip),
                                                        or_(Words.hebrewClean.contains(cleaned_word),
                                                            Words.arabicHebClean.contains(cleaned_word),
                                                            Words.arabicClean.contains(cleaned_word))
                                                        )).all()
            
            # CASE 2: "Soundex": Words sound like
            sound_index = get_sound_index(search_string_strip)
            if (len(sound_index)>0):
                with ArabicWordsDB() as arabic_words_db:
                    sound_like_words = arabic_words_db.session. \
                        query(Words.id, Words.show, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
                            Words.pronunciation).filter(and_(invalid_word_filter,
                                                            or_(Words.sndxArabicV1.like(f"%{sound_index}%"),
                                                                Words.sndxHebrewV1.like(f"%{sound_index}%"))
                                                            )).all()

            # CASE 3: "Like": Words with same letters
            with ArabicWordsDB() as arabic_words_db:
                letter_like_words = arabic_words_db.session. \
                    query(Words.id, Words.show, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
                        Words.pronunciation).filter(and_(invalid_word_filter,
                                                        Words.hebrewClean.like(f"%{cleaned_word}%")
                                                        )).all()

            # CASE 4: "SearchWords": Additional results: Typical errors, Synonyms
            with ArabicWordsDB() as arabic_words_db:
                search_words = arabic_words_db.session. \
                    query(Words.id, Words.show, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
                        Words.pronunciation).filter(and_(invalid_word_filter,
                                                        Words.searchString.like(f"%{search_string}%")
                                                        )).all()
            
            # DEBUG
            print(exact_match_words)
            print(sound_like_words)
            print(letter_like_words)
            print(search_words)
            
            # Remove duplications between lists!
            sound_like_words = [x for x in sound_like_words if x not in set(exact_match_words)]
            letter_like_words = [x for x in letter_like_words if x not in set(exact_match_words + sound_like_words)]
            search_words = [x for x in search_words if x not in set(exact_match_words + sound_like_words + letter_like_words)]

        #else:
        #     "ShortWords": One letter only
        #    with ArabicWordsDB() as arabic_words_db:
        #        short_words = arabic_words_db.session. \
        #            query(Words.id, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
        #                Words.pronunciation) \
        #                .filter(WordsShort.ID).all() \
        #                .filter(WordsShort.sStr == cleaned_word).all()
    else:
        if (len(cleaned_word) == 0) and (len(cleaned_word)>0):
            is_search_string_valid = False
  
    return render_template("default.html",
                           label_data_dicts=label_data_dicts,
                           is_search_string_valid=is_search_string_valid,
                           cleaned_word=cleaned_word,
                           sound_index=sound_index,
                           exact_match_words=exact_match_words,
                           sound_like_words=sound_like_words,
                           letter_like_words=letter_like_words,
                           search_words=search_words,
                           short_words=short_words)

if __name__ == '__main__':
    #app.run(host="192.168.2.109", port=5000, debug=True)
    #app.run(host="0.0.0.0", port=8081, debug=True)
    app.run(host="127.0.0.1", port=5431, debug=True)
