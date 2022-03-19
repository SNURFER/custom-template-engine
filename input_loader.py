import json


def load() -> json:
    f = open('input/data.json')
    users = json.load(f)
    f.close()

    return users
