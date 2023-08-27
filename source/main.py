from dataclasses import dataclass

from flask import Flask, redirect, url_for, request, render_template
from includes_utils import get_top_variables, get_trailer_variables
from utils import get_all_labels

app = Flask(__name__, template_folder="templates", static_folder="static")





@app.route("/labels.asp")
def labels_handler():
    all_labels = get_all_labels()


    return render_template("labels.html", labels=all_labels)



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
