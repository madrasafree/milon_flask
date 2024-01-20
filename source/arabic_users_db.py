import os
from dotenv import load_dotenv
from pathlib import Path
import json
from config.config import config

from sqlalchemy import Column, create_engine, inspect, UniqueConstraint, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP, BOOLEAN, INTEGER
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


class RelationTypes:
    SINGULAR_PLURAL = 3
    MALE_FEMALE = 4


Base = declarative_base()

PUBLIC_SCHEMA = {"schema": "public"}


# DEVELOPMENT SERVER CONFIGURATION:
load_dotenv()
user_name = "postgres"
password = config["DEV"].API_TOKEN   # TODO: ADD PASSWORD TO ENVIRONMENT VARIABLE UNDER "MADRASA_SERVER_KEY_SECRET_DEV"
# host_address = "arabic-words-db-server.c5cx9bfmz05i.us-east-1.rds.amazonaws.com"  # REMOTE PRODUCTION
# host_address = "localhost"                                                        # LOCAL DEVELOPMENT
host_address = "127.0.0.1"                                                          # LOCAL DEVELOPMENT
port = "5432"
#mdb = "arabic_words_db"
maintenance_database = "postgres"
db_connection_string = f"postgresql://{user_name}:{password}@{host_address}:{port}/{maintenance_database}"

class ArabicUsersDB:
    def __init__(self):
        self.session: AbstractSession = ...
        self.engine: Engine = ...

    def __enter__(self):
        self.engine = create_engine(db_connection_string)
        Session = sessionmaker(expire_on_commit=False)
        self.session = Session(bind=self.engine)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if not exception_type:
            self.session.commit()

        self.session.close()
        self.engine.dispose()


class AllowEdit(Base):
    __tablename__ = "allowEdit"
    __table_args__ = PUBLIC_SCHEMA
    siteName = Column(TEXT, primary_key=True)
    allowed = Column(TEXT)


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


class LoginLog(Base):
    __tablename__ = "loginLog"
    __table_args__ = PUBLIC_SCHEMA
    ID = Column(TEXT, primary_key=True)
    userID = Column(TEXT)
    loginTimeUTC = Column(TEXT)


class ListsUsers(Base):
    __tablename__ = "listsUsers"
    __table_args__ = PUBLIC_SCHEMA
    list = Column(TEXT, primary_key=True)
    user = Column(TEXT)
    pos = Column(TEXT)


class Users(Base):
    __tablename__ = "users"
    __table_args__ = PUBLIC_SCHEMA
    id = Column(TEXT, primary_key=True)
    userStatus = Column(TEXT)
    username = Column(TEXT)
    password = Column(TEXT)
    role = Column(TEXT)
    name = Column(TEXT)
    eMail = Column(TEXT)
    eMailVerify = Column(TEXT)
    eMailInterval = Column(TEXT)
    eMailInterval = Column(TEXT)
    about = Column(TEXT)
    gender = Column(TEXT)
    picture = Column(TEXT)
    joinDateUTC = Column(TEXT)
    maxLists = Column(TEXT)
    addWords = Column(TEXT)
    editorWords = Column(TEXT)
    editorPics = Column(TEXT)
    editorMedia = Column(TEXT)
    speaker = Column(TEXT)
    coder = Column(TEXT)
    arabicLevel = Column(TEXT)
    hebrewLevel = Column(TEXT)
    arabicDialect = Column(TEXT)
    arabicCity = Column(TEXT)
    credit = Column(TEXT)
    creditLink = Column(TEXT)


class UsersWordsFollow(Base):
    __tablename__ = "usersWordsFollow"
    __table_args__ = PUBLIC_SCHEMA
    userID = Column(TEXT, primary_key=True)
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
