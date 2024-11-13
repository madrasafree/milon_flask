from dataclasses import dataclass
from build.arabic_words_db import ArabicWordsDB, Labels, WordsLabels, Words, WordsShort, Sentences, WordsMedia, Media, Lists, ListsUsers, WordsLists
from build.arabic_users_db import ArabicUsersDB, AllowEdit, Log, LoginLog, Users, UsersWordsFollow
import config.config
import datetime
from datetime import timezone
import itertools
import library.functions
from flask import Flask, redirect, url_for, request, render_template, flash
from sqlalchemy import select, func, and_, or_, not_, cast, Integer, case
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    with ArabicUsersDB() as arabic_users_db:
        user = arabic_users_db.session.query(Users) \
            .filter(Users.id == id).first()
    return user


@dataclass
class Image:
    arabic: str
    arabicWord: str
    pronunciation: str
    hebrewTranslation: str
    hebrewDef: str
    imgLink: str
    imgCredit: str

def get_label_data_dicts(word_id = None):
    with ArabicWordsDB() as arabic_words_db:
        rows = arabic_words_db.session.query(Labels.ID, Labels.labelName).all()

    if (word_id != None):
        # Only labels with word_id
        with ArabicWordsDB() as arabic_words_db:
            wordsLabels = arabic_words_db.session.query(WordsLabels). \
                filter(WordsLabels.wordID == word_id).all() 
        labels = [x.labelID for x in wordsLabels if x.wordID == word_id]
    else:
        # All labels
        labels = [x.ID for x in rows] 

    label_data_dicts = []
    for label_row in rows:
        label_id = label_row.ID
        label_name = label_row.labelName

        if (label_id in labels):
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

@app.route("/labels.asp")
def labels_handler():
    label_data_dicts = get_label_data_dicts()

    return render_template("labels.html",
                            label_data_dicts = label_data_dicts)

@app.route("/label.asp")
def label_handler():
    label_id = request.args.get("id")
    if not label_id:
        label_id = "no label_id was found"

    label_data_dicts = get_label_data_dicts()

    with ArabicWordsDB() as arabic_words_db:
        row = arabic_words_db.session.query(Labels.labelName).filter(Labels.ID == label_id).one()
    label_name = row.labelName

    with ArabicWordsDB() as arabic_words_db:
        rows = arabic_words_db.session.query(WordsLabels.wordID).filter(WordsLabels.labelID == label_id).all()
    word_count = len(rows)
    all_label_word_ids = [row.wordID for row in rows]

    with ArabicWordsDB() as arabic_words_db:
        words = arabic_words_db.session.\
            query(Words.id, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef,
                  Words.pronunciation).filter(Words.id.in_(all_label_word_ids)).all()
    words.sort(key=lambda x: library.functions.get_clean_word(x.arabicWord)[0], reverse=False)

    return render_template("label.html",
                            label_data_dicts = label_data_dicts,
                            label_name = label_name,
                            word_count = word_count,
                            words = words)

@app.route("/lists.all.asp")
def lists_all_handler():
    list_id = request.args.get("id", "")
    is_search_submitted = (list_id != "")
    is_list_found = (not is_search_submitted)
    
    # Pull all Lists
    query_columns_lists = { Lists }
    with ArabicWordsDB() as arabic_words_db:
        lists_all = arabic_words_db.session.query(*query_columns_lists)    \
            .filter().all()
    lists_all = [list for list in lists_all if int(list.privacy) > 1]

    # Pull Top 10 Newest lists
    lists_top_new = lists_all
    lists_top_new.sort(key=lambda x: datetime.datetime.strptime(x.creationTimeUTC, "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    if (len(lists_top_new) > 10): lists_top_new = lists_top_new[:10]
    for l in lists_top_new:
        l.creationTimeUTC = str(datetime.datetime.fromisoformat(l.creationTimeUTC[:-1])).split()[0]

    # Pull Top 10 Viewed lists
    lists_top_view = lists_all
    lists_top_view.sort(key=lambda x: int(x.viewCNT), reverse=True)
    if (len(lists_top_view) > 10): lists_top_view = lists_top_view[:10]

    # Pull all Usernames
    query_columns_users = { Users.id, Users.username }
    with ArabicUsersDB() as arabic_users_db:
        users_all = arabic_users_db.session.query(*query_columns_users)    \
            .filter().all()
    lists_mine = []
    current_user_id = current_user.id if current_user.is_authenticated else -1
    for l in lists_all:
        if l.creator == current_user_id:
            lists_mine.append(l)
        l.creator = [user.username for user in users_all if (user.id == l.creator)][0]
    
    # Create list of Lists in alphabet order
    lists_all.sort(key=lambda x: x.listName, reverse=False)
    lists_all_alphabet = []
    for letter in itertools.groupby(lists_all, lambda x: x.listName[0]):
        lists_with_letter = list(letter[1])
        lists_all_alphabet.append(lists_with_letter)

    lists_favorite = []
    if current_user.is_authenticated:
        with ArabicWordsDB() as arabic_words_db:
            lists_favorite = read_favorites(current_user_id, arabic_words_db)
    # Reorganize Data
    lists_all_dict = {"lists_top_new": lists_top_new,
                    "lists_top_view": lists_top_view,
                    "lists_all_alphabet": lists_all_alphabet,
                    "lists_mine": lists_mine,
                    "lists_favorite": lists_favorite}

    return render_template("lists.all.html",
                                is_search_submitted = is_search_submitted,
                                is_list_found = is_list_found,
                                lists_all_dict = lists_all_dict)

def read_favorites(current_user_id, arabic_words_db):
    query_columns_lists = { Lists }
    lists_favorite_ids = arabic_words_db.session.query(ListsUsers.list) \
        .filter(ListsUsers.user == current_user_id) \
        .order_by(ListsUsers.pos).all()

    if not lists_favorite_ids:
        return lists_favorite_ids

    lists_favorite_ids = [item[0] for item in lists_favorite_ids]  # Assuming ListsUsers.list is a single column
    ordering = case(
        {id: pos for pos, id in enumerate(lists_favorite_ids)},
        value=ListsUsers.list
    )

    lists_favorite = arabic_words_db.session.query(*query_columns_lists) \
        .join(ListsUsers, Lists.ID == ListsUsers.list) \
        .filter(Lists.ID.in_(lists_favorite_ids)) \
        .order_by(ordering).all()

    return lists_favorite

@app.route("/lists.asp")
def lists_handler():
    list_id = request.args.get("id", "")
    is_search_submitted = (list_id != "")

    # Pull List
    query_columns_lists = { Lists }
    with ArabicWordsDB() as arabic_words_db:
        list_element = arabic_words_db.session.query(*query_columns_lists)    \
            .filter(Lists.ID == list_id).first()
    is_list_found = (list_element is not None)

    if (not is_search_submitted) or (is_search_submitted and not is_list_found):
        return redirect(f"lists.all.asp?id={list_id}", code=302)

    # Pull List's Creator
    query_columns_users = { Users }
    with ArabicUsersDB() as arabic_users_db:
        user = arabic_users_db.session.query(*query_columns_users)    \
            .filter(Users.id == list_element.creator).first()

    # Pull WordsIDs from List
    query_columns_wordsLists = { WordsLists.wordID }
    with ArabicWordsDB() as arabic_words_db:
        wordsLists = arabic_words_db.session.query(*query_columns_wordsLists)    \
            .filter(WordsLists.listID == list_id).all()

    # Pull Words from List
    words = []
    query_columns_words = { Words }
    for wordID in wordsLists:
        with ArabicWordsDB() as arabic_words_db:
            word = arabic_words_db.session.query(*query_columns_words)    \
                .filter(Words.id == wordID[0]).first()
        words.append(word)

    # Pull 7 most-recently-updated public lists from same creator
    with ArabicWordsDB() as arabic_words_db:
        moreLists = arabic_words_db.session.query(*query_columns_lists)    \
            .filter(Lists.creator == list_element.creator).all()
    moreLists = [l for l in moreLists if int(l.privacy) > 1]
    moreLists.sort(key=lambda x: datetime.datetime.strptime(x.lastUpdateUTC, "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    if (len(moreLists) > 10): moreLists = moreLists[:10]

    # Reorganize Data
    privacy_dict={
        0:["רשימה פרטית","lock"],
        1:["רשימה לבעלי קישור","lock_open"],
        2:["רשימה פומבית","public"],
        3:["רשימה משותפת","group"],
    }

    list_dict={
        "privacy_type": privacy_dict[int(list_element.privacy)][0],
        "privacy_icon": privacy_dict[int(list_element.privacy)][1],
        "listCreatorUsername" : user.username,
        "str2hebDate_lastUpdateUTC": library.functions.Str2hebDate(list_element.lastUpdateUTC),
        "str2hebDate_creationTimeUTC": library.functions.Str2hebDate(list_element.creationTimeUTC),
    }

    starred = False
    if current_user.is_authenticated:
        starred = check_starred(current_user.id, list_id)
    return render_template("lists.html",
                            is_search_submitted = is_search_submitted,
                            is_list_found = is_list_found,
                            list_id = list_id,
                            list_element = list_element,
                            list_dict = list_dict,
                            wordsLists = wordsLists,
                            words = words,
                            moreLists = moreLists,
                            starred = starred)

def check_starred(user_id, list_id):
    with ArabicWordsDB() as arabic_words_db:
        row_exists = arabic_words_db.session.query(ListsUsers) \
            .filter(ListsUsers.user == user_id, ListsUsers.list == list_id) \
            .first()

    return True if row_exists else False


@app.route("/sentences.asp")
def sentences_handler():
    with ArabicWordsDB() as arabic_words_db:
        sentence_count = arabic_words_db.session.query(func.count(Sentences.id)).scalar()

    #new query
    with ArabicWordsDB() as arabic_words_db:
        sentences = arabic_words_db.session.query(Sentences).all()

    return render_template("sentences.html",
                            sentence_count = sentence_count,
                            sentences = sentences)

@app.route("/guide.asp")
def guide_handler():
    return render_template("guide.html")

@app.route("/guideTeam.asp")
def guide_team_handler():
    return render_template("guideTeam.html")

@app.route("/welcome.asp")
def welcome_handler():
    return render_template("welcome.html")

@app.route("/clock.asp")
def clock_handler():
    return render_template("clock.html")

@app.route("/word.asp")
def word_handler():
    word_id = request.args.get("id", "")
    label_data_dicts = get_label_data_dicts(word_id)

    query_columns = { Words.id, Words.show, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef, Words.hebrewClean, Words.arabicClean, Words.arabicHebClean, Words.pronunciation,  \
                    Words.imgLink, Words.partOfSpeach, Words.gender, Words.number}

    with ArabicWordsDB() as arabic_words_db:
        word = arabic_words_db.session.query(*query_columns)    \
            .filter(and_(Words.id == word_id)).first()

    return render_template("word.html",
                            word_id = word_id,
                            word = word,
                            label_data_dicts = label_data_dicts)

@app.route("/about.asp")
def about_handler():
    return render_template("about.html")

@app.route("/games.mem.asp")
def games_mem_handler():
    with ArabicWordsDB() as arabic_words_db:
        results = arabic_words_db.session.query(Words).filter(
            Words.imgLink.isnot(None),
            Words.show == "1",
            Words.status == "1"
        ).order_by(func.random()).limit(20).all()
        images = [
            Image(
                arabic=result.arabic,
                arabicWord=result.arabicWord,
                pronunciation=result.pronunciation,
                hebrewTranslation=result.hebrewTranslation,
                hebrewDef=result.hebrewDef,
                imgLink=result.imgLink,
                imgCredit=result.imgCredit
            ) for result in results
        ]
        return render_template("games.mem.html", images=images)

@app.route("/")
@app.route("/default.asp")
def root_handler():
    # INITIALIZE VARIABLES
    is_search_submitted = True
    is_search_string_valid = True
    is_search_string_short = False
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
    cleaned_word = library.functions.get_clean_word(search_string_strip)

    #DEBUG
    #print("search_string = " + search_string)
    #print("search_string_strip = " + search_string_strip)
    #print("cleaned_word = " + cleaned_word)

    query_columns = { Words.id, Words.show, Words.arabic, Words.arabicWord, Words.hebrewTranslation, Words.hebrewDef, Words.hebrewClean, Words.arabicClean, Words.arabicHebClean, Words.pronunciation,  \
                        Words.imgLink}

    # TODO: Extract MEDIA
    # WordsMedia.wordID, WordsMedia.mediaID, Media.id

    invalid_word_filter = and_(
        Words.show == "True",
        Words.hebrewTranslation != "None",
        Words.arabic != "None",
        Words.arabicWord != "None"
    )

    if (len(search_string) == 0):
        is_search_submitted = False
        print("is_search_submitted = " + str(is_search_submitted))

    if (len(cleaned_word) == 0):
        # CASE -1: Invalid Search due to Symbols or foreign Language
        is_search_string_valid = False
        print("is_search_string_valid = " + str(is_search_string_valid))
    
    if (len(cleaned_word) == 1):
        # CASE 0: "ShortWords": One letter only
        is_search_string_short = True
        with ArabicWordsDB() as arabic_words_db:
            short_words = arabic_words_db.session.query(*query_columns)    \
                .filter(and_(invalid_word_filter,       # TODO: FIX!
                            or_(Words.hebrewClean == cleaned_word,
                                Words.arabicClean == cleaned_word,
                                Words.arabicHebClean == cleaned_word)
                            )).all()
                #.filter(WordsShort.ID).all() \
                #.filter(WordsShort.sStr == cleaned_word).all()

    if (len(cleaned_word)>1):
        # CASE 1: "Identical": Words exactly as searched
        with ArabicWordsDB() as arabic_words_db:
            exact_match_words = arabic_words_db.session.query(*query_columns)    \
                .filter(and_(invalid_word_filter,       # TODO: FIX!
                            or_(Words.hebrewClean == cleaned_word,
                                Words.arabicClean == cleaned_word,
                                Words.arabicHebClean == cleaned_word)
                            )).all()
        # CASE 2: "Soundex": Words sound like
        sound_index = library.functions.get_sound_index(search_string_strip)
        if (len(sound_index)>0):
            with ArabicWordsDB() as arabic_words_db:
                sound_like_words = arabic_words_db.session.query(*query_columns) \
                    .filter(and_(invalid_word_filter,
                                or_(Words.sndxArabicV1.like(f"%{sound_index}%"),
                                    Words.sndxHebrewV1.like(f"%{sound_index}%"))
                                )).all()
        # CASE 3: "Like": Words with same letters
        with ArabicWordsDB() as arabic_words_db:
            letter_like_words = arabic_words_db.session.query(*query_columns)    \
                    .filter(and_(invalid_word_filter,
                                Words.hebrewClean.like(f"%{cleaned_word}%")
                                )).all()
        # CASE 4: "SearchWords": Additional results: Typical errors, Synonyms
        with ArabicWordsDB() as arabic_words_db:
            search_words = arabic_words_db.session.query(*query_columns) \
                    .filter(and_(invalid_word_filter,
                                Words.searchString.like(f"%{search_string}%")
                                )).all()
        
        # DEBUG
        #print(exact_match_words)
        #print(sound_like_words)
        #print(letter_like_words)
        #print(search_words)
        # Remove duplications between lists!
        sound_like_words = [x for x in sound_like_words if x not in set(exact_match_words)]
        letter_like_words = [x for x in letter_like_words if x not in set(exact_match_words + sound_like_words)]
        search_words = [x for x in search_words if x not in set(exact_match_words + sound_like_words + letter_like_words)]
  
    return render_template("default.html",
                            search_string = search_string,
                            label_data_dicts = label_data_dicts,
                            is_search_submitted = is_search_submitted,
                            is_search_string_valid = is_search_string_valid,
                            is_search_string_short = is_search_string_short,
                            cleaned_word = cleaned_word,
                            sound_index = sound_index,
                            exact_match_words = exact_match_words,
                            sound_like_words = sound_like_words,
                            letter_like_words = letter_like_words,
                            search_words = search_words,
                            short_words = short_words)


@app.route("/login.asp", methods=['GET', 'POST'])
def login_handler():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with ArabicUsersDB() as arabic_users_db:
            user = arabic_users_db.session.query(Users) \
                .filter(Users.username == username, Users.password == password).first()
            if user:
                login_user(user)
                return redirect("/")
            return 'Invalid credentials'
    if current_user.is_authenticated:
        return redirect("/")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/listsToggle.asp')
def lists_toggle_handler():
    list_id = request.args.get("lid")
    if current_user.is_authenticated:
        if current_user.is_authenticated and list_id:
            with ArabicWordsDB() as arabic_words_db:
                is_starred = check_starred(current_user.id, list_id)
                if is_starred:
                    arabic_words_db.session.query(ListsUsers) \
                        .filter(ListsUsers.user == current_user.id, ListsUsers.list == list_id) \
                        .delete()
                else:
                    new_pos = int(get_max_pos(current_user.id, arabic_words_db)) + 1
                    new_list_user = ListsUsers(user=current_user.id, list=list_id, pos=new_pos)
                    arabic_words_db.session.add(new_list_user)
                arabic_words_db.session.commit()
    else:
        flash("יש להתחבר על מנת לשמור רשימה למועדפים")
    return redirect(f"lists.asp?id={list_id}", code=302)


@app.route("/listsNew.asp")
def listsNew_handler():
    if not current_user.is_authenticated:
        flash("על מנת לערוך רשימות, עליך להיות מחובר")
        return redirect("login.asp")
    if fetch_is_site_in_read_only_mode():
        flash("אין כרגע אפשרות ליצור רשימות חדשות. אנא נסו שנית מאוחר יותר")
        return redirect("/")
    with ArabicWordsDB() as arabic_users_db:
        user_id = current_user.id
        count = arabic_users_db.session.query(func.count(Lists.ID)).filter(Lists.creator == user_id).scalar()
        if count > int(current_user.maxLists):
            message = f"הגעת למספר הרשימות המקסימלי ({count}).</br>לא ניתן ליצור רשימה נוספת בשלב זה. מוזמן לפנות למנהל האתר לפרטים נוספים."
            flash(message)
            return redirect("lists.asp")
        return render_template('listsNew.html', listsCount=count, maxLists=current_user.maxLists)

@app.route("/listsNew.insert.asp", methods=["GET", "POST"])
def listsNewInsert_handler():
    if not current_user.is_authenticated:
        flash("אין לך הרשאה מתאימה")
        return redirect(request.referrer or '/')
    if fetch_is_site_in_read_only_mode():
        flash("אין כרגע אפשרות ליצור רשימות חדשות. אנא נסו שנית מאוחר יותר")
        return redirect("/")
    lTitle = request.form.get("lTitle")
    lDesc = request.form.get("lDesc")
    lPrivacy = 1
    lType = 10

    with ArabicWordsDB() as arabic_words_db:
        list_with_same_name_and_creator = arabic_words_db.session.query(Lists)\
            .filter(Lists.listName == lTitle, Lists.creator == current_user.id).first()
        if list_with_same_name_and_creator:
            flash("כבר יש לך רשימה עם אותו שם")
            redirect("listsNew.asp")
        current_max_id = arabic_words_db.session.query(func.max(cast(Lists.ID, Integer))).scalar()
        new_list_id = int(current_max_id) + 1
        now = datetime.datetime.now(timezone.utc)
        new_list = Lists(ID=new_list_id,
                         creator=current_user.id,
                         listName=lTitle,
                         privacy=lPrivacy,
                         type=lType,
                         listDesc=lDesc,
                         creationTimeUTC=now,
                         lastUpdateUTC=now
                         )
        arabic_words_db.session.add(new_list)
        arabic_words_db.session.commit()
        flash("הרשימה נוספה בהצלחה")
        return redirect(f"lists.asp?id={new_list_id}")

def fetch_is_site_in_read_only_mode():
    with ArabicUsersDB() as arabic_users_db:
        readonly_site = arabic_users_db.session.query(AllowEdit).filter(AllowEdit.siteName == 'readOnly').first()
        return readonly_site and readonly_site.allowed == "1"

def get_max_pos(user_id, arabic_words_db):
    max_pos = arabic_words_db.session.query(func.max(ListsUsers.pos)) \
        .filter(ListsUsers.user == user_id) \
        .scalar()
    return max_pos if max_pos is not None else 0


if __name__ == '__main__':
    app.run(host=config.config.host_address, port=config.config.port_app, debug=True)
