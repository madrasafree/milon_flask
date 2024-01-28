import config.config

from sqlalchemy import Column, create_engine, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP, BOOLEAN, INTEGER
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

class RelationTypes:
    SINGULAR_PLURAL = 3
    MALE_FEMALE = 4

Base = declarative_base()
PUBLIC_SCHEMA = {"schema": "public"}

class ArabicWordsDB:
    def __init__(self):
        self.session: AbstractSession = ...
        self.engine: Engine = ...

    def __enter__(self):
        self.engine = create_engine(config.config.db_connection_string)
        Session = sessionmaker(expire_on_commit=False)
        self.session = Session(bind=self.engine)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if not exception_type:
            self.session.commit()

        self.session.close()
        self.engine.dispose()

class History(Base):
    __tablename__ = "history"
    __table_args__ = PUBLIC_SCHEMA
    ID = Column(TEXT, primary_key=True)
    word = Column(TEXT)
    actionUTC = Column(TEXT)
    action = Column(TEXT)
    user = Column(TEXT)
    statusOld = Column(TEXT)
    statusNew = Column(TEXT)
    errorTypes = Column(TEXT)
    explain = Column(TEXT)
    showOld = Column(TEXT)
    showNew = Column(TEXT)
    hebrewOld = Column(TEXT)
    hebrewNew = Column(TEXT)
    hebrewDefOld = Column(TEXT)
    hebrewDefNew = Column(TEXT)
    arabicOld = Column(TEXT)
    arabicNew = Column(TEXT)
    arabicWordOld = Column(TEXT)
    arabicWordNew = Column(TEXT)
    pronunciationOld = Column(TEXT)
    pronunciationNew = Column(TEXT)
    searchStringOld = Column(TEXT)
    searchStringNew = Column(TEXT)
    rootOld = Column(TEXT)
    rootNew = Column(TEXT)
    partOfSpeachOld = Column(TEXT)
    partOfSpeachNew = Column(TEXT)
    binyanOld = Column(TEXT)
    binyanNew = Column(TEXT)
    genderOld = Column(TEXT)
    genderNew = Column(TEXT)
    numberOld = Column(TEXT)
    numberNew = Column(TEXT)
    infoOld = Column(TEXT)
    infoNew = Column(TEXT)
    exampleOld = Column(TEXT)
    exampleNew = Column(TEXT)
    imgLinkOld = Column(TEXT)
    imgLinkNew = Column(TEXT)
    imgCreditOld = Column(TEXT)
    imgCreditNew = Column(TEXT)
    linkDescOld = Column(TEXT)
    linkDescNew = Column(TEXT)
    linkOld = Column(TEXT)
    linkNew = Column(TEXT)
    labelsOld = Column(TEXT)
    labelsNew = Column(TEXT)

class Labels(Base):
    __tablename__ = "labels"
    __table_args__ = PUBLIC_SCHEMA
    ID = Column(TEXT, primary_key=True)
    labelName = Column(TEXT)
    fbIMG = Column(TEXT)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Lists(Base):
    __tablename__ = "lists"
    __table_args__ = PUBLIC_SCHEMA
    ID = Column(TEXT, primary_key=True)
    creator = Column(TEXT)
    listName = Column(TEXT)
    listDesc = Column(TEXT)
    viewCNT = Column(TEXT)
    creationTimeUTC = Column(TEXT)
    lastUpdateUTC = Column(TEXT)
    privacy = Column(TEXT)
    type = Column(TEXT)

class ListsUsers(Base):
    __tablename__ = "listsUsers"
    __table_args__ = PUBLIC_SCHEMA
    list = Column(TEXT, primary_key=True)
    user = Column(TEXT)
    pos = Column(TEXT)

class Log(Base):
    __tablename__ = "log"
    __table_args__ = PUBLIC_SCHEMA
    ID = Column(TEXT, primary_key=True)
    opType = Column(TEXT)
    afDB = Column(TEXT)
    afPage = Column(TEXT)
    opNum = Column(TEXT)
    userIP = Column(TEXT)
    opTimestamp = Column(TEXT)
    durationMs = Column(TEXT)
    sStr = Column(TEXT)

class Media(Base):
    __tablename__ = "media"
    __table_args__ = PUBLIC_SCHEMA
    id = Column(TEXT, primary_key=True)
    mType = Column(TEXT)
    mLink = Column(TEXT)
    description = Column(TEXT)
    credit = Column(TEXT)
    creditLink = Column(TEXT)
    speaker = Column(TEXT)
    uploader = Column(TEXT)
    school = Column(TEXT)
    creationTime = Column(TEXT)
    creationTimeUTC = Column(TEXT)
    lastUpdateUTC = Column(TEXT)

class Sentences(Base):
    __tablename__ = "sentences"
    __table_args__ = PUBLIC_SCHEMA
    id = Column(TEXT, primary_key=True)
    show = Column(TEXT)
    status = Column(TEXT)
    hebrew = Column(TEXT)
    hebrewClean = Column(TEXT)
    arabic = Column(TEXT)
    arabicClean = Column(TEXT)
    arabicHeb = Column(TEXT)
    arabicHebClean = Column(TEXT)
    info = Column(TEXT)
    creator = Column(TEXT)
    creationTimeUTC = Column(TEXT)

class Words(Base):
    __tablename__ = "words"
    __table_args__ = PUBLIC_SCHEMA
    id = Column(TEXT, primary_key=True)
    show = Column(TEXT)  # bool, show/hide
    status = Column(TEXT)  # nidak, lo nivdak, hasad le'taut
    lockedUTC = Column(TEXT)
    isLocked = Column(TEXT)
    hebrewTranslation = Column(TEXT)
    hebrewClean = Column(TEXT)
    hebrewCleanMore = Column(TEXT)  # extra for search
    hebrewDef = Column(TEXT)  # perushon
    sndxHebrewV1 = Column(TEXT)  # sound index
    arabic = Column(TEXT)
    arabicClean = Column(TEXT)
    arabicCleanMore = Column(TEXT)
    sndxArabicV1 = Column(TEXT)
    arabicWord = Column(TEXT)  # transliterated
    arabicHebClean = Column(TEXT)   # transliterated
    arabicHebCleanMore = Column(TEXT)   # transliterated
    pronunciation = Column(TEXT)
    searchString = Column(TEXT)  # like hebrewCleanMore
    originWordID = Column(TEXT)  # Unknown
    partOfSpeach = Column(TEXT)
    gender = Column(TEXT)
    number = Column(TEXT)
    binyan = Column(TEXT)
    info = Column(TEXT)
    example = Column(TEXT)
    creatorID = Column(TEXT)
    creationTimeUTC = Column(TEXT)
    imgLink = Column(TEXT)
    imgCredit = Column(TEXT)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class WordsLabels(Base):
    __tablename__ = "wordsLabels"
    #__table_args__ = PUBLIC_SCHEMA
    wordID = Column(TEXT)
    labelID = Column(TEXT)
    __table_args__ = (
        PrimaryKeyConstraint(wordID, labelID),
    )

class WordsLists(Base):
    __tablename__ = "wordsLists"
    #__table_args__ = PUBLIC_SCHEMA
    wordID = Column(TEXT)
    listID = Column(TEXT)
    pos = Column(TEXT)
    __table_args__ = (
        PrimaryKeyConstraint(wordID, listID),
    )
    
class WordsMedia(Base):
    __tablename__ = "wordsMedia"
    #__table_args__ = PUBLIC_SCHEMA
    wordID = Column(TEXT)
    mediaID = Column(TEXT)
    __table_args__ = (
        PrimaryKeyConstraint(wordID, mediaID),
    )

class WordsRelations(Base):
    __tablename__ = "wordsRelations"
    __table_args__ = PUBLIC_SCHEMA
    word1 = Column(TEXT, primary_key=True)
    word2 = Column(TEXT)
    relationType = Column(TEXT)

class WordsSentences(Base):
    __tablename__ = "wordsSentences"
    __table_args__ = PUBLIC_SCHEMA
    word = Column(TEXT, primary_key=True)
    sentence = Column(TEXT)
    location = Column(TEXT)
    relevance = Column(TEXT)
    merge = Column(TEXT)

class WordsShort(Base):
    __tablename__ = "wordsShort"
    __table_args__ = PUBLIC_SCHEMA
    ID = Column(TEXT, primary_key=True)
    sStr = Column(TEXT)
    wordID = Column(TEXT)

class QueryOptions:
    @staticmethod
    def all():
        pass

    @staticmethod
    def first():
        pass

    @staticmethod
    def one():
        pass

    @staticmethod
    def count():
        pass

    @staticmethod
    def order_by(*args):
        pass

class Filterable:
    @staticmethod
    def filter(*args, **kwargs) -> QueryOptions:
        return ...

    @staticmethod
    def all():
        pass

class AbstractSession(Session):
    @staticmethod
    def query(*args, **kwargs) -> Filterable:
        return ...