"""Модуль для подключения к БД и оределения класов таблиц БД"""
# Данные для подключения к базе данных

from sqlalchemy import Column, ForeignKey, Integer,\
    String, Float, Boolean, DateTime, engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
# from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import MetaData, Table


from data import config
HOST = config.HOST
USER = config.USER
PASSWORD = config.PASSWORD
DB = config.DB
engine =  create_engine(
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DB}",
    echo=False)

"""
engine =  create_engine(
    f"mysql+mysqlconnector://dmartinchick:samsungLX40@localhost/svarog2022_db",
    echo=True)
"""
Base = declarative_base()
metadata = MetaData(bind=engine)


ass_user_event = Table('user_event', Base.metadata,
    Column('user_id', ForeignKey('user.user_id'), primary_key=True),
    Column('event_id', ForeignKey('event.id'), primary_key=True)
)

ass_user_team = Table('user_team', Base.metadata,
    Column('user_id', ForeignKey('user.user_id'), primary_key=True),
    Column('team_id', ForeignKey('team.id'), primary_key=True)
)


class User(Base):
    """Определение класса User
    TODO: изменить поле admin на statute"""

    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=False)
    admin = Column(Boolean, default=False)
    event = relationship('Event', secondary=ass_user_event, backref='user')
    team = relationship('Team', secondary=ass_user_team, backref='user')


class Event(Base):
    """Определение класса Event"""
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_type = Column(String)
    coefficient = Column(Float)
    place = Column(String)
    rule = Column(String)
    composition = Column(String)
    address = Column(String)
    name_en = Column(String)
    schedule = relationship('Schedule')
    results = relationship('Results')


class Team(Base):
    """Определение класса Team"""
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    holding = Column(Boolean)
    address = Column(String)
    name_en = Column(String)
    results = relationship('Results')


class Schedule(Base):
    """Определение класса Schedule"""
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'))
    time_start = Column(DateTime)
    time_end = Column(DateTime)


class Results(Base):
    """Определение класса Results"""
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'))
    team_id = Column(Integer, ForeignKey('team.id'))
    place = Column(Integer)


Base.metadata.create_all(engine)
