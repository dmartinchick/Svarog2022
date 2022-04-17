"""Функции для работы с БД"""

from datetime import datetime
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_, desc
from sqlalchemy.orm.session import Session

from utils.db_api.sqlalch import Event, Results, Schedule, Team, User, \
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
    for admin in s.query(User.user_id).filter(User.admin == 1).all():
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
        Team.id).order_by(Team.name).all():
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


def get_team_id(name_en: str) -> int:
    """Возвращает id команды по обращению через name_en

    Args:
        name_en (str): название команды на английском языке

    Returns:
        int: id команды
    """
    team_id = s.query(Team.id)\
        .filter(Team.name_en == name_en)\
            .first()
    return team_id[0]


def get_team_name(team_id: int) -> str:
    """Возвращает название команды по ID

    Args:
        team_id (int): ID команды

    Returns:
        str: Название команды
    """
    team_name = s.query(Team.name).filter(Team.id == team_id).first()
    return team_name[0]


def get_event_name(event_id: int) -> str:
    """Возвращает название конкурса по ID

    Args:
        event_id (int): ID конкурса

    Returns:
        str: название конкруса
    """
    event_name = s.query(Event.name).filter(Event.id == event_id).first()
    return event_name[0]


def count_teams() -> int:
    """Возвращает количество команд на фестивале

    Returns:
        int: Кол-во команд
    """
    count = s.query(Team.id).count()
    return count


def get_result_list() -> list:
    """возвращает список конкурсов на которые уже введены результаты

    Returns:
        list: Список конкурсов с внесенными результатами
    TODO: Добавить event_name
    """
    result_list = []

    for result in s.query(Results.event_id).distinct().all():
        result_list.append(result[0])

    return result_list


def get_event_results(event_id:int) -> list:
    """Возвращает пользователю словарь с результатами выбранного конкурса

    Args:
        event_id (int): id конкурса

    Returns:
        list: список словарей с результатами конкурса
    """
    event_results = []
    for result in s.query(Results.id ,Results.team_id, Results.place).\
        where(Results.event_id == event_id).all():
        event_results.append(
            {
                'result_id' : result[0],
                'team_name' : get_team_name(result[1]),
                'place' : result[2]
            }
        )
    return event_results


def get_team_name_from_result(reslt_id:int) -> str:
    """Возвращает название команды по id результата

    Args:
        reslt_id (int): id результата

    Returns:
        str: название команды
    """
    team_id = s.query(Results.team_id).\
        where(Results.id == reslt_id).one()
    team_name = get_team_name(int(team_id[0]))
    return team_name


def get_schedule_list() -> list:
    """Возвращает пользователю список словорей с данными о расписании

    Returns:
        list: список словарей с данными о расписании
    """
    schedule_list = []
    for event in s.query(
        Schedule.id,
        Schedule.event_id,
        Schedule.time_start,
        Schedule.time_end).all():
        schedule_list.append(
            {'schedule_id' : event[0],
            'event_id' : event[1],
            'event_name' : get_event_name(event[1]),
            'start' : event[2].strftime("%d.%m %H:%M"),
            'end' : event[3].strftime("%d.%m %H:%M")}
        )
    return schedule_list


def get_schedule_event_name(schedule_id:int) -> str:
    """Возвращает названия мероприятия из расписания

    Args:
        schedule_id (int): id пункта расписания

    Returns:
        str: названия мероприятия
    """
    event_id = s.query(Schedule.event_id).where(Schedule.id == schedule_id).one()
    event_name = s.query(Event.name).where(Event.id == event_id[0]).one()
    return event_name[0]


def get_result(cup:str = None, holding:bool=None) -> list:
    """Возвращает список словарей с результатами и вспомогательными данными

    Returns:
        list: список словарей
    """
    result_list = []
    # Проверяем переданно ли значение cup
    if cup is None:
        if holding is None:
            # Проверяем переданно ли значение holding
            results = s.query(
                Results.event_id,
                Event.name,
                Event.event_type,
                Event.coefficient,
                Results.team_id,
                Team.name,
                Team.holding,
                Results.place
            ).join(Event, Event.id == Results.event_id).\
                join(Team, Team.id == Results.team_id).all()
        else:
            results = s.query(
                Results.event_id,
                Event.name,
                Event.event_type,
                Event.coefficient,
                Results.team_id,
                Team.name,
                Team.holding,
                Results.place
            ).join(Event, Event.id == Results.event_id).\
                join(Team, Team.id == Results.team_id).\
                    filter(Team.holding).all()
    else:
        results = s.query(
            Results.event_id,
            Event.name,
            Event.event_type,
            Event.coefficient,
            Results.team_id,
            Team.name,
            Team.holding,
            Results.place
        ).join(Event, Event.id == Results.event_id).\
            join(Team, Team.id == Results.team_id).\
                filter(Event.event_type == cup).all()

    for result in results:
        result_list.append(
            {'event_id' : result[0],
            'event_name' : result[1],
            'cup' : result[2],
            'event_coefficient' : result[3],
            'team_id' : result[4],
            'team_name' : result[5],
            'team_holding' : result[6],
            'place' : result[7]}
        )
    return result_list


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


def set_results(results: dict):
    """Добавляет результат в БД

    Args:
        event_id (int): id конкурса
        team_id (int): id команды
        place (int): место которое заняла команда
    """
    event_id = results['event_id']
    results_list = list(results.items())[1:]
    for item in results_list:
        result = Results(
            event_id = event_id,
            team_id = item[1]['team_id'],
            place = item[1]['place']
        )
        s.add(result)
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


def delete_event_result(event_id:int):
    """Удаляет результаты конкурса из БД

    Args:
        event_id (int): id конкурса
    """
    delete_event = delete(Results).\
        where(Results.event_id == event_id)
    s.execute(delete_event)
    s.commit()


# Функции изменения данных
def set_update_result(result_id:int, place:int):
    """Обновляет результат команды в таблице Results

    Args:
        reslt_id (int): id результата
        place (int): обновленное место команды
    """
    s.query(Results).where(Results.id == result_id).\
        update({Results.place : place}, synchronize_session = False)
    s.commit()


def set_update_schedule(schedule_id:int, star:datetime, end:datetime):
    """Обновляет время начала и окончания мероприятия

    Args:
        schedule_id (int): id мероприятия
        star (datetime): обновленная дата и время начала мероприятия
        end (datetime): обновленная дата и время окончания мероприятия
    """
    s.query(Schedule).where(Schedule.id == schedule_id).\
        update({Schedule.time_start : star,
        Schedule.time_end :end}, synchronize_session = False)
    s.commit()
