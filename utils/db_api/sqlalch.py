"""Модуль для подключения к БД и оределения класов таблиц БД"""
# Данные для подключения к базе данных
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Float, Text, DateTime, engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import MetaData, Table

from data import config
HOST = config.HOST
USER = config.USER
PASSWORD = config.PASSWORD
DB = config.DB
engine =  create_engine(
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DB}",
    echo=False)

"""engine =  create_engine(
    f"mysql+mysqlconnector://dmartinchick:samsungLX40@localhost/svarog2022_db",
    echo=False)
"""

Base = declarative_base()
metadata = MetaData(bind=engine)

class Event(Base):
    """Определение класа Event"""
    __tablename__ = Table("Event", metadata, autoload=True)

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum('Кубок спорта', 'Кубок туризма', 'Кубок культуры', 'Прочее'), nullable=False)
    coefficient = Column(Float(2,1))
    place = Column(String(255))
    rule = Column(Text)
    composition = Column(String(255))
    address = Column(String(255))
    name_en = Column(String(255))


    def __init__(self, name, type, coefficient, place, rule, composition, address, name_en) -> None:
        self.name = name
        self.type = type
        self.coefficient = coefficient
        self.place = place
        self.rule = rule
        self.composition = composition
        self.address = address
        self.name_en = name_en


class Team(Base):
    """Определение класса Team"""
    __tablename__ = Table("Team", metadata, autoload=True)

    id = Column(Integer,primary_key=True)
    name = Column(String(100), nullable=False)
    holding = Column(Integer, nullable=False)
    address = Column(String(255))

    def __init__(self, name, holding, address):
        self.name = name
        self.holding = holding
        self.address = address

    def __repr__(self):
        return "Team (name = '%s', holding = '%s', address = '%s')"%(
            self.name,
            self.holding,
            self.address)


class User(Base):
    """Определение класса User"""
    __tablename__ = Table("User", metadata, autoload=True)

    user_id = Column(Integer, primary_key=True, autoincrement=False)

    def __init__(self, user_id):
        self.user_id = user_id


class Results(Base):
    """Определение класса Resilts"""
    __tablename__ = Table("Results", metadata, autoload=True)

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("Team.id"), nullable=False)
    evet_id = Column(Integer, ForeignKey("Event.id"), nullable=False)
    results = Column(Integer)

    def __init__(self, team_id, event_id, results):
        self.team_id = team_id
        self.evet_id = event_id
        self.results = results


class Schedule(Base):
    """Определение класса Shedule"""
    __tablename__ = Table("Schedule", metadata, autoload=True)

    id = Column(Integer, primary_key=True)
    event_id  =Column(Integer, ForeignKey("Event.id"), nullable=False)
    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=False)

    def __init__(self, event_id, time_start, time_end) -> None:
        self.event_id = event_id
        self.time_start = time_start
        self.time_end = time_end


class Subscriptions(Base):
    """Определение класса Subscriptions"""
    __tablename__ = Table("Subscriptions", metadata, autoload=True)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    team_id = Column(Integer, ForeignKey("Team.id"))
    event_id = Column(Integer, ForeignKey("Event.id"))

    def __init__(self, user_id, team_id, event_id) -> None:
        self.user_id = user_id
        self.team_id = team_id
        self.event_id = event_id


Base.metadata.create_all(engine)
