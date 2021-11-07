"""Вспомогательные функции"""

def check_item_id(item_id:str, items_list:list):
    """Проверяет есть подписан ли пользователь на item_id

    Args:
        item_id (str): id кнкурса или команды
        items_list (list): список подписок пользователя на конкурсы или команды

    Returns:
        [type]: [description]
    """
    for item in items_list:
        if item['item_id'] == item_id:
            return True
    return False
