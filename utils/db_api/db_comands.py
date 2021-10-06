from datetime import datetime
from aiogram.types.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.sql.expression import and_, desc
from sqlalchemy.orm.session import Session
from utils.db_api.sqlalch import Base, Event, Schedule, Team, User

from data.config import USER, PASSWORD, HOST, DB

engine =  create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DB}", echo=False)
# engine =  create_engine(f"mysql+mysqlconnector://dmartinchick:samsungLX40@localhost/svarog2022_db", echo=True)

Session = sessionmaker(bind=engine)
s = Session()

"""
rq = s.query(Schedule.time_start).order_by(Schedule.time_start).first()
print(rq)
"""

# методы извлечения данных

def get_date_start():
    """Возвращает пользователю дату начала фестиваля

    Returns:
        [type]: [description]
    """
    rq = s.query(Schedule.time_start).order_by(Schedule.time_start).first()
    return rq[0]


def get_date_end():

    rq = s.query(Schedule.time_end).order_by(desc(Schedule.time_end)).first()
    return rq[0]


def get_what_now(tdate):
    # TODO: добавить поля с картинкой, временем оканчания
    rq = s.query(Event.name).filter(and_(Schedule.event_id == Event.id, Schedule.time_start > tdate)).limit(1)
    return rq


def get_what_next(tdate):
    # TODO: добавить поля с картинкой, временем оканчания
    next_event_list = []
    for item in s.query(Event.name, Schedule.time_start).filter(and_(Schedule.event_id == Event.id, Schedule.time_start > tdate)).order_by(Schedule.time_start).limit(2):
        event_dict = {'name':item[0], 'time_start':item[1]}
        next_event_list.append(event_dict)
    return next_event_list


def get_full_shedule():
    event_list = []
    for event in s.query(Event.name, Schedule.time_start, Schedule.time_end).filter(and_(Schedule.event_id == Event.id, Event.type != "Прочее")).all():
        event_dict = {'name':event[0], 'time_start':event[1], 'time_end':event[2]}
        event_list.append(event_dict)
    return event_list


def get_event_info(event_id):
    rq = s.qery(Event.name, Event.type, Event.coefficient, Event.rule, Event.composition, Schedule.time_start).filtre(and_(Schedule.event_id == Event.id, Event.id ==event_id)).one()
    event_info = {'name':rq[0], 'type':rq[1], 'coefficient':rq[2], 'rule':rq[3], 'composition':rq[4], 'time_start':rq[5]}
    return event_info

def get_users_list():
    users_list = []
    for user in s.query(User.user_id).all():
        users_list.append(user[0])
    
    return users_list


def get_team_all():

    team_list = []
    for team in s.query(Team.name, Team.id).all:
        team_list.append({'name':team[0], 'id':team[1]})
    
    return team_list


# Методы добавления данных
def set_user(user_id):
    user = User(user_id)
    s.add(user)
    s.commit()