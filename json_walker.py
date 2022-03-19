import json


def find_val(user: json, key_list: []) -> str:
    new_json = user
    while len(key_list) > 1:
        key = key_list.pop(0)
        if key in new_json:
            new_json = new_json[key]

    return new_json[key_list[-1]]


