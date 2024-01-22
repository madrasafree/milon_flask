import datetime
import re

#'SOUND_INDEX_FUNCTIONS'

def get_clean_word(word):
    cleaned_word = re.sub(r"[^א-ת'ؠ-يٱ-ٳٶ-ە]", "", word)
    return cleaned_word

def get_sound_index(word):

    sound_index = ""
    letters = word
    dbl = False
    # Removes chars which aren't Hebrew or Arabic letters, or Geresh
    letters = re.sub(r"[^א-ת'ؠ-يٱ-ٳٶ-ە]", "", letters)

    for character_index, character in enumerate(letters):
        next_char = character_index + 1
        if dbl:
            dbl = False
        elif character in ["א", "ו", "י"]:
            if character_index > 0:
                sound_index += "" # hebrew a'he'vi
            else:
                if character in ["א"]:
                    sound_index += "A"
                elif character in ["ו"]:
                    sound_index += "W"
                else:
                    sound_index += "Y"
        elif character in ["צ", "ץ", "ד"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "D"
            dbl = True
        elif character in ["ט"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "S"
            dbl = True
        elif character in ["ת"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "T"
            dbl = True
        elif character in ["ה", "ח"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "H"
            dbl = True
        elif character in ["ג", "ז"] and next_char < len(word) and word[character_index + 1] == "'":
            sound_index += "J"
            dbl = True
        elif character in ["ר"] and next_char < len(word) and word[character_index + 1] == "'":
            sound_index += "R"
            dbl = True
        # arabic letters
        elif character in ["ا", "آ", "أ", "إ", "ئ", "ة", "ء", "ؤ", "ي", "ى", "و"]:
            sound_index += ""
        elif character in ["د", "ד", "ذ", "ד'", "ض", "צ'", "ץ'", ]:
            sound_index += "D"
        elif character in ["ص", "צ", "ץ", "س", "ס", "ز", "ז", "ظ", "ט'"]:
            sound_index += "S"
        elif character in ["ط", "ט", "ت", "ת", "ث", "ת'"]:
            sound_index += "T"
        elif character in ["ب", "ב"]:
            sound_index += "B"
        elif character in ["ن", "נ", "ן"]:
            sound_index += "N"
        elif character in ["ع", "ע"]:
            sound_index += "A"
        elif character in ['ة', 'ه', "ה", "ה'", "ح", "ח", "ח'", "خ"]:
            sound_index += "H"
        elif character in ["ك", "כ", "ך", "ق", "ק", "ג"]:
            sound_index += "K"
        elif character in ["ش", "ש", "ج", "ג'", "ז'"]:
            sound_index += "J"
        elif character in ["غ", "ע'", "ر", "ר", "ר'"]:  # TODO "ע'" not working
            sound_index += "R"
        elif character in ["ل", "ל"]:
            sound_index += "L"
        elif character in ["م", "מ", "ם"]:
            sound_index += "M"
        elif character in ["ف", "פ", "ף"]:
            sound_index += "F"
        else:
            sound_index += character

    return sound_index


assert get_sound_index("עיתונות") == "ATNT"
assert get_sound_index("עזר") == "ASR"
assert get_sound_index("שכל") == "JKL"
assert get_sound_index("כאפיה") == "KFH"
assert get_sound_index("החלטה") == "HHLTH"


#'TIME FUNCTIONS'
#'version 2020-05-05 21:05'

#'NOTE: GoDaddy Servers go by Arizona Time - GMT-7

# !!! THIS FUNCTION IS REPLACED By AR2UTC !!!!
def isrTime():
    # ADD 9 HOURS TO now()
    # info: GoDaddy's Server is 9 hours behind Israel's time
    if str(Request.ServerVariables("http_host"))[:5] == "ronen":
        isrTime = DateAdd("h", 9, now())
    else:
        isrTime = now()

def iso2nums(str):
    x = str
    if len(x) > 0:
        x = x.replace("T", "")
        x = x.replace("-", "")
        x = x.replace(":", "")
        x = x.replace("Z", "")
    else:
        x = 0
    # x = CInt(trim(x))
    iso2nums = x

def intToStr(num, length):
    # NUM to STRING
    # Add 0 before single characters
    # info: helps keep date in ISO8601 format [yyyy-mm-ddThh:mm:ssZ]
    x = str(num)
    x = x.rjust(length, "0")
    intToStr = x

def date_to_str_ISO8601(date):
    # use str() function to change entire date to string
    y = str(date.year) + "-" + str(date.month).zfill(2) + "-" + str(date.day).zfill(2) + "T" + str(date.hour).zfill(2) + ":" + str(date.minute).zfill(2) + ":" + str(date.second).zfill(2) + "Z"
    return y

# REPLACED by dateToStrISO8601
def dateToStr(date):
    # use str() function to change entire date to string
    y = str(date.year) + "-" + str(date.month).zfill(2) + "-" + str(date.day).zfill(2) + " " + str(date.hour).zfill(2) + ":" + str(date.minute).zfill(2) + ":" + str(date.second).zfill(2)
    return y

def AR2UTC(date):
    # Receive date from server (in Arizona time - UTC-7)
    # Use str() function to format date as string according to ISO8601 + UTC: YYYY-MM-DDTHH:MM:SSZ
    u = date + datetime.timedelta(hours=7)  # add 7 hours
    y = str(u.year) + "-" + str(u.month).zfill(2) + "-" + str(u.day).zfill(2) + "T" + str(u.hour).zfill(2) + ":" + str(u.minute).zfill(2) + ":" + str(u.second).zfill(2) + "Z"
    return y

# prints STRING as Hebrew Date
def Str2hebDate(strDate):
    if (strDate == "" or strDate == "None"):
        return ""
    day = strDate[8:10] + " ל"
    month = strDate[5:7]
    if month == "01":
        monthStr = "ינואר"
    elif month == "02":
        monthStr = "פברואר"
    elif month == "03":
        monthStr = "מרץ"
    elif month == "04":
        monthStr = "אפריל"
    elif month == "05":
        monthStr = "מאי"
    elif month == "06":
        monthStr = "יוני"
    elif month == "07":
        monthStr = "יולי"
    elif month == "08":
        monthStr = "אוגוסט"
    elif month == "09":
        monthStr = "ספטמבר"
    elif month == "10":
        monthStr = "אוקטובר"
    elif month == "11":
        monthStr = "נובמבר"
    elif month == "12":
        monthStr = "דצמבר"
    else:
        monthStr = month
    year = (" " + strDate[:4])
    return day + monthStr + year



