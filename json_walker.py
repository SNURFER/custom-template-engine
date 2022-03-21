import json


def find_val(data: json, key_list: []) -> str:
    if len(key_list) == 0 and type(data) != str:
        return '?'

    new_data = data
    while len(key_list) > 0:
        key = key_list.pop(0)
        if key in new_data:
            new_data = new_data[key]
        elif key.isdigit():
            if len(new_data) <= int(key):
                return '?'
            new_data = new_data[int(key)]
        else:
            return '?'

    return new_data


def find_arr(data: json, key_list: []) -> []:
    new_data = data
    while len(key_list) > 0:
        key = key_list.pop(0)
        if key in new_data:
            new_data = new_data[key]
        elif key.isdigit():
            if len(new_data) <= int(key):
                return '?'
            new_data = new_data[int(key)]
        elif key == '*':
            # every array elements
            new_data = [element for element in new_data]
        else:
            new_data = [element[key] for element in new_data]

    return new_data
