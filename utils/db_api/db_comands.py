"""Функции для работы с БД"""

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_, desc
from sqlalchemy.orm.session import Session

from utils.db_api.sqlalch import Event, Schedule, Team, User, \
    ass_user_event, ass_user_team

from data.config import USER, PASSWORD, HOST, DB

engine =  create_engine(
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DB}",
    echo=False
    )

"""engine =  create_engine(
    f"mysql+mysqlconnector://dmartinchick:samsungLX40@localhost/svarog2022_db",
    echo=True
    )
"""

Session = sessionmaker(bind=engine)
s = Session()
"""
#user_id = 466138751
rq = s.query(User).all()
print(rq)
"""

# Функции извлечения данных

def get_date_start():
    """Возвращает пользователю дату начала фестиваля

    Returns:
        dt_start_request[datetime]: дата и время первого события фестиваля
    """
    dt_start_request = s.query(
        Schedule.time_start
        ).order_by(
            Schedule.time_start
            ).first()
    return dt_start_request[0]


def get_date_end():
    """Возвращает пользователю дату и время конца фестиваля

    Returns:
        dt_end_request[datetime]: дата и время последнего события фестиваля
    """
    dt_end_request = s.query(
        Schedule.time_end
        ).order_by(
            desc(Schedule.time_end)
            ).first()
    return dt_end_request[0]


def get_what_now(tdate) -> list:
    """Возвращает пользователю список событий, которые происходят в настоящий момент

    Args:
        tdate (datetime): текущее время и дата

    Returns:
        now_event_list [list]: Список событий

    """
    now_event_list = []
    for item in s.query(
        Event.name,
        Event.id,
        Schedule.time_end,
        Event.address).filter(
            and_(
                Schedule.event_id == Event.id,
                Schedule.time_start < tdate,
                Schedule.time_end > tdate)).all():
        now_event_list.append(
            {'name':item[0],
            'event_id':item[1],
            'time_end':item[2],
            'adress_photo':item[3]})

    return now_event_list


def get_what_next(tdate) -> list:
    """Возвращает пользователю список словарей 2-х ближайших событий

    Args:
        tdate (daettime): Текущее время и дату

    Returns:
        list: список из ближайших событий

    """
    next_event_list = []
    for item in s.query(
        Event.name,
        Event.id,
        Schedule.time_start,
        Event.address).filter(
            and_(
                Schedule.event_id == Event.id,
                Schedule.time_start > tdate)).order_by(
                    Schedule.time_start).limit(2):
        next_event_list.append(
            {'name':item[0],
            'event_id':item[1],
            'event_time_start':item[2],
            'adress_photo':item[3]}
            )
    return next_event_list


def get_full_shedule() -> list:
    """Возвращает пользователю полное расписание

    Returns:
        list: список словарей с полным расписанием

    """
    event_list = []
    for event in s.query(
        Event.name,
        Schedule.time_start,
        Schedule.time_end).filter(
            and_(
                Schedule.event_id == Event.id,
                Event.event_type != "Прочее")).all():
        event_dict = {
            'name':event[0],
            'time_start':event[1],
            'time_end':event[2]
            }
        event_list.append(event_dict)
    return event_list


def get_event_info(event_id:int) -> dict:
    """Возвращает пользователю информацию о событии

    Args:
        event_id (int): индификатор события

    Returns:
        dict: словарь с информацие о конкурсе
    """
    event_info_request = s.query(
        Event.name,
        Event.event_type,
        Event.coefficient,
        Event.rule,
        Event.composition,
        Schedule.time_start,
        Event.address).filter(
            and_(
                Schedule.event_id == Event.id,
                Event.id ==event_id)).first()
    event_info = {
        'name':event_info_request[0],
        'type':event_info_request[1],
        'coefficient':event_info_request[2],
        'rule':event_info_request[3],
        'composition':event_info_request[4],
        'time_start':event_info_request[5],
        'adress_photo':event_info_request[6]
        }
    return event_info


def get_team_info(team_id:int) ->dict:
    """Возвращает пользователю информацию о команде

    Args:
        team_id (int): id команды

    Returns:
        dict: словарь с информацией о конкурся
    """
    team_info_request = s.query(
        Team.name,
        Team.holding).filter(
            Team.id == team_id
        ).one()
    team_info={
        'name' : team_info_request[0],
        'holding' : team_info_request[1]
    }
    return team_info


def get_events_list() -> list:
    """Возвращает пользователю список конкурсов

    Returns:
        list: список словарей конкурсов

    """
    event_list = []
    for event in s.query(
        Event.name,
        Event.id).filter(
            Event.event_type != "Прочее"):
        event_list.append(
            {'name' : event[0],
            'item_id' : event[1]})
    return event_list


def get_users_list() -> list:
    """Возвращает список пользователей

    Returns:
        list: список пользователей
    """
    users_list = []
    for user in s.query(User.user_id).all():
        users_list.append(user[0])
    return users_list

def get_admin_list() -> list:
    """Функция возвращает список администраторов

    Returns:
        list: список администраторов
    """
    admin_list = []
    for admin in s.query(User.user_id).filter(User.admin is True).all():
        admin_list.append(admin[0])
    return admin_list


def get_teams_list() -> list:
    """Возвращает спискок всех команд

    Returns:
        list: список словарей все команд
    """
    team_list = []
    for team in s.query(
        Team.name,
        Team.id).all():
        team_list.append(
            {'name':team[0],
            'item_id':team[1]})
    return team_list


def get_signed_teams_list(user_id: int) -> list:
    """Возвращает список команд на которые подписан пользователь

    Args:
        user_id (int): id пользователя

    Returns:
        list: список словарей на которые подписан пользователь

    """
    signed_teams_list = []

    teams = s.query(Team.name, Team.id)\
        .join(User.team)\
            .filter(User.user_id == user_id)
    for team in teams:
        signed_teams_list.append(
            {
                'name':team[0],
                'item_id':team[1]
            }
        )

    return signed_teams_list


def get_signed_events_list(user_id: int) -> list:
    """Возвращает список конкурсов на которые подписан пользователь

    Args:
        user_id (int): id пользователя

    Returns:
        list: список словарей конкурсов на которые подписан пользователь
    """
    signed_events_list = []

    events = s.query(Event.name, Event.id)\
        .join(User.event)\
            .filter(User.user_id == user_id)

    for event in events:
        signed_events_list.append(
            {'name': event[0], 'item_id':event[1]}
        )

    return signed_events_list


# Функции добавления данных
def set_user(user_id):
    """Добавлеят пользователя в БД

    Args:
        user_id (int): id пользователя
    """
    user = User(user_id)
    s.add(user)
    s.commit()


def set_sign_to_event(user_id:int, event_id:int):
    """Добавляет подписку на события

    Args:
        user_id (int): id пользователя
        event_id (int): id конкурса
    """
    s.execute(ass_user_event\
        .insert()\
            .values(
                user_id = user_id,
                event_id = event_id))
    s.commit()


def set_sign_to_team(user_id:int, team_id:int):
    """Добавляет подписку на команды

    Args:
        user_id (int): id пользователя
        team_id (int): id команды
    """
    s.execute(ass_user_team\
        .insert()\
            .values(
                user_id = user_id,
                team_id = team_id))
    s.commit()


# Функции для удаления данных
def set_unsing_to_event(user_id: int, event_id:int):
    """удаляет запись о подписке на конкурс из БД

    Args:
        user_id (int): id пользователя
        event_id (int): id конкурса

    """
    unsigned_event = delete(ass_user_event).\
        where(
            ass_user_event.c.user_id == user_id,
            ass_user_event.c.event_id == event_id
        ).\
            execution_options(
                synchronize_session = "False"
            )

    s.execute(unsigned_event)
    s.commit()


def set_unsing_to_team(user_id:int, team_id:int):
    """Удаляет запись о подписке на команду из БД

    Args:
        user_id (int): id пользователя
        team_id (int): id команды

    """
    unsigned_team = delete(ass_user_team).\
        where(
            ass_user_team.c.user_id == user_id,
            ass_user_team.c.team_id == team_id
        ).\
            execution_options(
                synchronize_session="False"
            )

    s.execute(unsigned_team)
    s.commit()
