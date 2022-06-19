"""Вспомогательные функции"""
from datetime import datetime
from data.config import TZ


def get_tdate():
    """Функция возвращает скоректированное значение даты и времени
    """
    tdelta = datetime.now(TZ).utcoffset()
    tdate = datetime.now() + tdelta
    return tdate
