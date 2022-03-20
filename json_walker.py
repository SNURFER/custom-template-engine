import json


def find_val(user: json, key_list: []) -> str:
    new_json = user
    while len(key_list) > 0:
        key = key_list.pop(0)
        if key in new_json:
            new_json = new_json[key]
        elif key.isdigit():
            if len(new_json) <= int(key):
                return '?'
            new_json = new_json[int(key)]
        else:
            return '?'

    return new_json


def find_arr(user: json, key_list: []) -> []:
    new_json = user
    while len(key_list) > 0:
        key = key_list.pop(0)
        if key in new_json:
            new_json = new_json[key]
        elif key.isdigit():
            if len(new_json) <= int(key):
                return '?'
            new_json = new_json[int(key)]
        elif key == '*':
            # every array elements
            new_json = [element for element in new_json]
        else:
            new_json = [element[key] for element in new_json]

    return new_json
