# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from .settings import DATABASE

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**DATABASE))


def create_apps_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Apps(DeclarativeBase):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    url = Column('url', String, nullable=True)
    virus = Column('virus', String, nullable=True)
    ad = Column('ad', String, nullable=True)
    file_paths = Column('file_paths', String, nullable=True)