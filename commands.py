def remove(document, command):
    path_to_remove = command['path'].split('/')[1]
    print(path_to_remove)
    try:
        del document[path_to_remove]
    except KeyError:
        return {}, f"Can't remove not exist object: {path_to_remove}."
    return document, ""


def add(document, command):
    return document, ""


def move(document, command):
    return document, ""


def replace(document, command):
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
