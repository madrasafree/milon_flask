from dataclasses import dataclass

from flask import Flask, redirect, url_for, request, render_template
from sqlalchemy import func
from arabic_words_db import ArabicWordsDB, Labels, WordsLabels
from includes_utils import get_top_variables, get_trailer_variables


app = Flask(__name__, template_folder="templates", static_folder="static")

# """  case x>=0 AND x<=10
#             tagSize = "0.8em"
#             case x>=11 AND x<=30
#             tagSize = "1em"
#             case x>=31 AND x<=70
#             tagSize = "1.3em"
#             case x>=71 AND x<=120
#             tagSize = "1.5em"
#             case x>=121 AND x<=180
#             tagSize = "1.7em"
#             case x>=180 AND x<=300
#             tagSize = "1.9em"
#             case else
#             tagSize = "2.4em""""


@app.route("/labels.asp")
def labels_handler():

    with ArabicWordsDB() as arabic_words_db:
        rows = arabic_words_db.session.query(Labels.ID, Labels.labelName).all()

    label_data_dicts = []
    for label_row in rows:
        label_id = label_row.ID
        label_name = label_row.labelName

        with ArabicWordsDB() as arabic_words_db:
            word_count = arabic_words_db.session.query(func.count(WordsLabels.wordID)).\
                filter(WordsLabels.labelID == label_id).scalar()

            if word_count <= 10:
                tag_size = "0.8em"
            elif 11 <= word_count <= 30:
                tag_size = "1em"
            else:
                tag_size = "2.4em"

        label_data_dict = {}
        label_data_dict["name"] = label_name
        label_data_dict["title"] = f"there are {word_count} words in this topic"
        label_data_dict["href"] = f"label.asp?id={label_id}"
        label_data_dict["style_string"] = f"font-size:{tag_size}"

        label_data_dicts.append(label_data_dict)

    return render_template("labels.html", label_data_dicts=label_data_dicts)



#http://localhost:8081/label.asp?id=5


@app.route("/label.asp")
def label_handler():
    label_id = request.args.get("id")
    if not label_id:
        label_id = "no word_id was found"

    all_labels = get_all_labels()

    label_name = "food"


    return render_template("label.html",  labels=all_labels, label_id=label_id, label_name=label_name)



@app.route("/guide.asp")
def guide_handler():
    return render_template("guide.html")


@dataclass
class Image:
    arabic: str
    arabicWord: str



@app.route("/games.mem.asp")
def games_mem_handler():

    image1 = Image("cat", "biss")
    image2 = Image("school", "madrasa")

    images = [image1, image2]
    return render_template("games.mem.html", images=images)








if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
