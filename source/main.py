from flask import Flask, redirect, url_for, request, render_template
from dataclasses import dataclass
from includes_utils import get_top_variables, get_trailer_variables

app = Flask(__name__, template_folder="templates", static_folder="static")

html_string = """<div id="tagsCloud">
<ul>
<li style="font-size:2.4em;" title="ישנן 308 מילים בנושא זה">
<a href="label.asp?id=5">אוכל</a>
</li>
<li style="font-size:1.9em;" title="ישנן 239 מילים בנושא זה">
<a href="label.asp?id=17">בבית</a>
</li>
<li style="font-size:1.5em;" title="ישנן 79 מילים בנושא זה">
<a href="label.asp?id=15">בגדים</a>
</li>
<li style="font-size:1.5em;" title="ישנן 101 מילים בנושא זה">
<a href="label.asp?id=36">ביטויים</a>
</li>
<li style="font-size:1.5em;" title="ישנן 77 מילים בנושא זה">
<a href="label.asp?id=33">בעלי חיים 1 - יונקים</a>
</li>
<li style="font-size:1.3em;" title="ישנן 35 מילים בנושא זה">
<a href="label.asp?id=39">בעלי חיים 2 - עופות</a>
</li>
<li style="font-size:1.5em;" title="ישנן 111 מילים בנושא זה">
<a href="label.asp?id=6">בעלי חיים 3 - כל השאר</a>
</li>
<li style="font-size:1.5em;" title="ישנן 102 מילים בנושא זה">
<a href="label.asp?id=4">ברכות</a>
</li>
<li style="font-size:1.3em;" title="ישנן 65 מילים בנושא זה">
<a href="label.asp?id=21">בשימוש בעברית</a>
</li>
<li style="font-size:1.7em;" title="ישנן 145 מילים בנושא זה">
<a href="label.asp?id=18">גוף האדם</a>
</li>
<li style="font-size:1.3em;" title="ישנן 65 מילים בנושא זה">
<a href="label.asp?id=31">דקדוק</a>
</li>
<li style="font-size:1.9em;" title="ישנן 214 מילים בנושא זה">
<a href="label.asp?id=20">דתות וחגים</a>
</li>
<li style="font-size:1.9em;" title="ישנן 182 מילים בנושא זה">
<a href="label.asp?id=7">זמן</a>
</li>
<li style="font-size:1.3em;" title="ישנן 51 מילים בנושא זה">
<a href="label.asp?id=28">חומרים</a>
</li>
<li style="font-size:1.5em;" title="ישנן 91 מילים בנושא זה">
<a href="label.asp?id=24">חינוך</a>
</li>
<li style="font-size:1.5em;" title="ישנן 93 מילים בנושא זה">
<a href="label.asp?id=38">טכנולוגיה ומחשבים</a>
</li>
<li style="font-size:1.3em;" title="ישנן 37 מילים בנושא זה">
<a href="label.asp?id=34">ירקות</a>
</li>
<li style="font-size:1em;" title="ישנן 28 מילים בנושא זה">
<a href="label.asp?id=37">כלי עבודה</a>
</li>
<li style="font-size:1.7em;" title="ישנן 166 מילים בנושא זה">
<a href="label.asp?id=16">כלכלה</a>
</li>
<li style="font-size:1.5em;" title="ישנן 77 מילים בנושא זה">
<a href="label.asp?id=23">מדע</a>
</li>
<li style="font-size:1.3em;" title="ישנן 53 מילים בנושא זה">
<a href="label.asp?id=32">מוסיקה</a>
</li>
<li style="font-size:1.5em;" title="ישנן 75 מילים בנושא זה">
<a href="label.asp?id=14">מזג אוויר</a>
</li>
<li style="font-size:1.3em;" title="ישנן 65 מילים בנושא זה">
<a href="label.asp?id=1">מספרים</a>
</li>
<li style="font-size:1.3em;" title="ישנן 48 מילים בנושא זה">
<a href="label.asp?id=29">מקומות 1 - מדינות</a>
</li>
<li style="font-size:1em;" title="ישנן 24 מילים בנושא זה">
<a href="label.asp?id=30">מקומות 2 - ערים</a>
</li>
<li style="font-size:1.9em;" title="ישנן 222 מילים בנושא זה">
<a href="label.asp?id=3">מקומות 3 - כל השאר</a>
</li>
<li style="font-size:1.9em;" title="ישנן 215 מילים בנושא זה">
<a href="label.asp?id=9">מקצועות</a>
</li>
<li style="font-size:1.5em;" title="ישנן 106 מילים בנושא זה">
<a href="label.asp?id=8">משפחה</a>
</li>
<li style="font-size:1.5em;" title="ישנן 117 מילים בנושא זה">
<a href="label.asp?id=13">ספורט</a>
</li>
<li style="font-size:1.9em;" title="ישנן 190 מילים בנושא זה">
<a href="label.asp?id=11">פוליטיקה</a>
</li>
<li style="font-size:1.3em;" title="ישנן 59 מילים בנושא זה">
<a href="label.asp?id=35">פירות</a>
</li>
<li style="font-size:1.7em;" title="ישנן 166 מילים בנושא זה">
<a href="label.asp?id=12">צבא וביטחון</a>
</li>
<li style="font-size:1.3em;" title="ישנן 36 מילים בנושא זה">
<a href="label.asp?id=2">צבעים</a>
</li>
<li style="font-size:1.3em;" title="ישנן 59 מילים בנושא זה">
<a href="label.asp?id=19">צמחים</a>
</li>
<li style="font-size:1.9em;" title="ישנן 204 מילים בנושא זה">
<a href="label.asp?id=22">רפואה</a>
</li>
<li style="font-size:1.3em;" title="ישנן 55 מילים בנושא זה">
<a href="label.asp?id=10">שאלות</a>
</li>
<li style="font-size:1.3em;" title="ישנן 53 מילים בנושא זה">
<a href="label.asp?id=25">שמות פרטיים</a>
</li>
<li style="font-size:1.5em;" title="ישנן 110 מילים בנושא זה">
<a href="label.asp?id=26">תחבורה</a>
</li>
<li style="font-size:1.3em;" title="ישנן 63 מילים בנושא זה">
<a href="label.asp?id=27">תקשורת</a>
</li>
</ul>
</div>"""


from bs4 import BeautifulSoup

soup = BeautifulSoup(html_string, parser="lxml")
@dataclass
class Label:
    name: str
    title: str
    href: str
    style_string: str

labels = []

for li_tag in soup.find_all("li"):

    style_string = li_tag["style"]
    title = li_tag["title"]
    a_tag = li_tag.find("a")
    href = a_tag["href"]
    name = a_tag.string
    label = Label(name, title, href, style_string)
    labels.append(label)





@app.route("/")
def hello_name():
    # word_id = request.args.get("id")
    # if not word_id:
    #     word_id = "no word_id was found"

    trailer_variable = get_trailer_variables()

    return render_template("labels.html", labels=labels, **trailer_variable)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)



"""



"""