"""Вспомогательные функции"""
from datetime import datetime
from data.config import TZ
from utils.db_api.db_comands import get_events_id, get_results, get_teams_id


def get_tdate() -> datetime:
    """Функция возвращает скоректированное значение даты и времени
    """
    tdelta = datetime.now(TZ).utcoffset()
    tdate = datetime.now() + tdelta
    return tdate

def make_data_results():
    """Функция проходится по всем конкурсам и всем командам и заполняет недостающие значения

    Args:
        events (_type_): _description_
        teams (_type_): _description_

    Returns:
        _type_: _description_
    """
    events = get_events_id()
    teams = get_teams_id()
    results = get_results()
    data_results = {}

    for event in events:
        for team in teams:
            data_results.update({(event, team): results.get((event, team), '-')})

    return data_results
