"""Вспомогательные функции"""


def get_unsubs_list(list_all:list, list_subs:list) -> list:
    """Отбирает из полного списка команд или конкурсов те,
         на которые не подписан пользователь

    Args:
        list_all (list): Полный список команд или конкурсов
        list_subs (list): Список команд или конкурсов на которые подписан пользователь

    Returns:
        list: список словарей команд или конкурсов  на которые не подписан пользователь
    """
    user_unsubs = []
    for item in list_all:
        if item not in list_subs:
            user_unsubs.append(item)

    return user_unsubs


def convert_to_list(user_tuple:tuple) -> list:
    """ПРеобразует тип tuple в list

    Args:
        user_tuple (tuple): пользовательский кортеж

    Returns:
        list: преобразованый пользовательский список
    """
    list_result = []
    for item in user_tuple:
        list_result.append({'name':item[0], 'id':item[1]})
    return list_result
