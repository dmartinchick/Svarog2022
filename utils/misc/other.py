def get_unsubs_list(list_all, list_subs):
    user_unsubs = []
    for item in list_all:
        if item not in list_subs:
            user_unsubs.append(item)

    return user_unsubs


def convert_to_list(tuple):
    list_result = []
    for item in tuple:
        list_result.append({'name':item[0], 'id':item[1]})
    return list_result