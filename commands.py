def remove(document, command):
    path_to_remove = command['path'].split('/')[1]
    try:
        del document[path_to_remove]
    except KeyError:
        return {}, f"Can't remove not exist object: {path_to_remove}."
    return document, ""


def add(document, command):
    path_to_add = command['path'].split('/')[1]
    if path_to_add in document.keys():
        return {}, f"Can't add existing path."
    path_value = command['value']
    document[path_to_add] = path_value
    return document, ""


def move(document, command):
    from_path = command['from'].split('/')[1]
    to_path = command['path'].split('/')[1]
    try:
        value_to_move = document[from_path]
    except KeyError:
        return {}, "Can't move from not exist path."
    document[from_path] = []
    try:
        document[to_path].extend(value_to_move)
    except KeyError:
        return {}, "Can't move to not exist path."
    return document, ""


def replace(document, command):
    path = command['path'].split('/')
    path_to_replace = path[1]
    index_to_replace = path[2]
    value = command['value']
    try:
        document[path_to_replace][int(index_to_replace)] = value
    except IndexError:
        return {}, "Can't replace not existing object."
    except KeyError:
        return {}, "Can't replace not existing path."
    return document, ""


def copy(document, command):
    return document, ""


def test(document, command):
    return document, ""


commands_functions = {"remove": remove,
                      "add": add,
                      "move": move,
                      "replace": replace,
                      "copy": copy,
                      "test": test}
