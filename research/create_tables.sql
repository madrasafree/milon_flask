-- This SQL script should be manually loaded to the DEV Local Server via pgAdmin 4 
-- This must be performed before one can load the data via milon_flask/source/scripts/import_db_from_windows.py


--------------------------
--- ArabicWords TABLES ---
--------------------------

create table if not exists "history"
(
	"ID"  text,
	"word"  text,
	"actionUTC"  text,
	"action"  text,
	"user"  text,
	"statusOld"  text,
	"statusNew"  text,
	"errorTypes"  text,
	"explain"  text,
	"showOld"  text,
	"showNew"  text,
	"hebrewOld"  text,
	"hebrewNew"  text,
	"hebrewDefOld"  text,
	"hebrewDefNew"  text,
	"arabicOld"  text,
	"arabicNew"  text,
	"arabicWordOld"  text,
	"arabicWordNew"  text,
	"pronunciationOld"  text,
	"pronunciationNew"  text,
	"searchStringOld"  text,
	"searchStringNew"  text,
	"rootOld"  text,
	"rootNew"  text,
	"partOfSpeachOld"  text,
	"partOfSpeachNew"  text,
	"binyanOld"  text,
	"binyanNew"  text,
	"genderOld"  text,
	"genderNew"  text,
	"numberOld"  text,
	"numberNew"  text,
	"infoOld"  text,
	"infoNew"  text,
	"exampleOld"  text,
	"exampleNew"  text,
	"imgLinkOld"  text,
	"imgLinkNew"  text,
	"imgCreditOld"  text,
	"imgCreditNew"  text,
	"linkDescOld"  text,
	"linkDescNew"  text,
	"linkOld"  text,
	"linkNew"  text,
	"labelsOld"  text,
	"labelsNew"  text
);

create table if not exists "labels"
(
	"ID"  text,
	"labelName"  text,
	"fbIMG"  text
);

create table if not exists "lists"
(
	"ID"  text,
	"creator"  text,
	"listName"  text,
	"listDesc"  text,
	"viewCNT"  text,
	"creationTimeUTC"  text,
	"lastUpdateUTC"  text,
	"privacy"  text,
	"type"  text
);

create table if not exists "listsUsers"
(
	"list"  text,
	"user"  text,
	"pos"  text
);

create table if not exists "log"
(
	"ID"  text,
	"opType"  text,
	"afDB"  text,
	"afPage"  text,
	"opNum"  text,
	"userIP"  text,
	"opTimestamp"  text,
	"durationMs"  text,
	"sStr"  text
);

create table if not exists "media"
(
	"id"  text,
	"mType"  text,
	"mLink"  text,
	"description"  text,
	"credit"  text,
	"creditLink"  text,
	"speaker"  text,
	"uploader"  text,
	"school"  text,
	"creationTime"  text,
	"creationTimeUTC"  text,
	"lastUpdateUTC"  text
);

create table if not exists "sentences"
(
	"id"  text,
	"show"  text,
	"status"  text,
	"hebrew"  text,
	"hebrewClean"  text,
	"arabic"  text,
	"arabicClean"  text,
	"arabicHeb"  text,
	"arabicHebClean"  text,
	"info"  text,
	"creator"  text,
	"creationTimeUTC"  text
);

create table if not exists "words"
(
	"id"  text,
	"show"  text,
	"status"  text,
	"lockedUTC"  text,
	"isLocked"  text,
	"hebrewTranslation"  text,
	"hebrewClean"  text,
	"hebrewCleanMore"  text,
	"hebrewDef"  text,
	"sndxHebrewV1"  text,
	"arabic"  text,
	"arabicClean"  text,
	"arabicCleanMore"  text,
	"sndxArabicV1"  text,
	"arabicWord"  text,
	"arabicHebClean"  text,
	"arabicHebCleanMore"  text,
	"pronunciation"  text,
	"searchString"  text,
	"originWordID"  text,
	"partOfSpeach"  text,
	"gender"  text,
	"number"  text,
	"binyan"  text,
	"info"  text,
	"example" text,
	"creationTimeUTC" text,
	"imgCredit" text,
	"creatorID" text,
	"imgLink" text
);

create table if not exists "wordsLabels"
(
	"wordID"  text,
	"labelID"  text
);

create table if not exists "wordsLists"
(
	"wordID"  text,
	"listID"  text,
	"pos"  text
);

create table if not exists "wordsMedia"
(
	"wordID"  text,
	"mediaID"  text
);

create table if not exists "wordsRelations"
(
	"word1"  text,
	"word2"  text,
	"relationType"  text
);

create table if not exists "wordsSentences"
(
	"word"  text,
	"sentence"  text,
	"location"  text,
	"relevance"  text,
	"merge"  text
);

create table if not exists "wordsShort"
(
	"ID"  text,
	"sStr"  text,
	"wordID"  text
);

--------------------------
--- ArabicUsers TABLES ---
--------------------------

create table if not exists "allowEdit"
(
	"siteName"  text,
	"allowed"  text
);

create table if not exists "log"
(
	"ID"  text,
	"opType"  text,
	"afDB"  text,
	"afPage"  text,
	"opNum"  text,
	"userIP"  text,
	"opTimestamp"  text,
	"durationMs"  text,
	"sStr"  text
);

create table if not exists "loginLog"
(
	"ID"  text,
	"userID"  text,
	"loginTimeUTC"  text
);

create table if not exists "users"
(
	"list"  text,
    "id"  text,
    "userStatus"  text,
    "username"  text,
    "password"  text,
    "role"  text,
    "name"  text,
    "eMail"  text,
    "eMailVerify"  text,
    "eMailLast"  text,
    "eMailInterval"  text,
    "about"  text,
    "gender"  text,
    "picture"  text,
    "joinDateUTC"  text,
    "maxLists"  text,
    "addWords"  text,
    "editorWords"  text,
    "editorPics"  text,
    "editorMedia"  text,
    "speaker"  text,
    "coder"  text,
    "arabicLevel"  text,
    "hebrewLevel"  text,
    "arabicDialect"  text,
    "arabicCity"  text,
    "credit"  text,
    "creditLink"  text
);

create table if not exists "usersWordsFollow"
(
	"userID"  text,
	"wordID"  text
);
