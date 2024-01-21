#'TIME FUNCTIONS'
#'version 2020-05-05 21:05'
import re
import datetime

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



