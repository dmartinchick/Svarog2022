"""Функции для работы с БД"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_, desc
from sqlalchemy.orm.session import Session

from utils.db_api.sqlalch import Event, Schedule, Team, User, \
    ass_user_event, ass_user_team
from utils.misc.other import get_unsubs_list

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

#user_id = 466138751
rq = s.query(User).all() 
print(rq)


# методы извлечения данных

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
    TODO: добавить поля с картинкой, временем оканчания
    """
    now_event_list = []
    for item in s.query(
        Event.name,
        Event.id,
        Schedule.time_end).filter(
            and_(
                Schedule.event_id == Event.id,
                Schedule.time_start < tdate,
                Schedule.time_end > tdate)).all():
        now_event_list.append(
            {'name':item[0],
            'event_id':item[1],
            'event_time_end':item[2]})

    return now_event_list


def get_what_next(tdate) -> list:
    """Возвращает пользователю список словарей 2-х ближайших событий

    Args:
        tdate (daettime): Текущее время и дату

    Returns:
        list: список из ближайших событий
    TODO: добавить поля с картинкой, временем оканчания
    """
    next_event_list = []
    for item in s.query(
        Event.name,
        Event.id,
        Schedule.time_start).filter(
            and_(
                Schedule.event_id == Event.id,
                Schedule.time_start > tdate)).order_by(
                    Schedule.time_start).limit(2):
        next_event_list.append(
            {'name':item[0],
            'event_id':item[1],
            'event_time_start':item[2]}
            )
    return next_event_list


def get_full_shedule() -> list:
    """Возвращает пользователю полное расписание

    Returns:
        list: список словарей с полным расписанием
    
    TODO: filter(and_(Schedule.event_id == Event.id, Event.event_type != "Прочее"))
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
        Schedule.time_start).filter(
            and_(
                Schedule.event_id == Event.id,
                Event.id ==event_id)).one()
    event_info = {
        'name':event_info_request[0],
        'type':event_info_request[1],
        'coefficient':event_info_request[2],
        'rule':event_info_request[3],
        'composition':event_info_request[4],
        'time_start':event_info_request[5]
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
    
    TODO: Не работает. filter(Event.event_type != "Прочее") 
    """
    event_list = []
    for event in s.query(
        Event.name,
        Event.id).filter(
            Event.event_type != "Прочее").all():
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
    TODO: Не работает. Проблема в filter(ass_user_team == user_id)
    """
    signed_teams_list = []
    for team in s.query(
        Team.name,
        Team.id).filter(ass_user_team.user_id == user_id).all():
        signed_teams_list.append(
            {'name': team[0], 'item_id':team[1]})

    return signed_teams_list


def get_unsigned_teams_list(user_id:int) -> list:
    """Возвращает список команд на которые не подписан пользователь

    Args:
        user_id (int): id пользователя

    Returns:
        list: список словарей на которые не подписан пользователь
    """
    team_list = get_teams_list()
    signed_teams_list = get_signed_teams_list(user_id)
    unsigned_teams_list = get_unsubs_list(team_list, signed_teams_list)
    return unsigned_teams_list


def get_signed_events_list(user_id: int) -> list:
    """Возвращает список конкурсов на которые подписан пользователь

    Args:
        user_id (int): id пользователя

    Returns:
        list: список словарей конкурсов на которые подписан пользователь
    
    #TODO: Не работает. Проблема в filter(ass_user_event == user_id)
    """
    signed_events_list = []
    for event in s.query(
        Event.name,
        Event.id).filter(
            ass_user_event.user_id == user_id).all():
        signed_events_list.append(
            {'name': event[0], 'item_id':event[1]})

    return signed_events_list


def get_unsigned_events_list(user_id:int) -> list:
    """Возвращает список конкурсов на которые не подписан пользователь

    Args:
        user_id (int): id пользователя

    Returns:
        list: список словарей на которые не подписан пользователь
    """
    events_list = get_events_list()
    signed_events_list = get_signed_events_list(user_id)
    unsigned_events_list = get_unsubs_list(events_list, signed_events_list)
    return unsigned_events_list


# Методы добавления данных
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
    s.execute(ass_user_event.insert().values(user_id, event_id))
    s.commit()


def set_sign_to_team(user_id:int, team_id:int):
    """Добавляет подписку на команды

    Args:
        user_id (int): id пользователя
        team_id (int): id команды
    TODO: не добавляет данные. AttributeError: 'Session' object has no attribute 'comit'
    """
    s.execute(ass_user_team.insert().values(user_id = user_id, team_id = team_id))


# Функции для удаления данных
def set_unsing_to_event(user_id: int, event_id:int):
    """удаляет запись о подписке на конкурс из БД

    Args:
        user_id (int): id пользователя
        event_id (int): id конкурса
    
    TODO: Реализовать функцию
    """
    pass


def set_unsing_to_team(user_id:int, team_id:int):
    """Удаляет запись о подписке на команду из БД

    Args:
        user_id (int): id пользователя
        team_id (int): id команды
    
    TODO: Реализовать функцию
    """
    pass
