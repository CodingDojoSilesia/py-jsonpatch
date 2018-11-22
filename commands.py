def remove(document, command):
    path_to_remove = command['path'].split('/')[1]
    try:
        del document[path_to_remove]
    except KeyError:
        return {}, f"Can't remove not exist object: {path_to_remove}."
    return document, ""


def add(document, command):
    """
    Adds a value to an object or inserts it into an array.
    :param document:
    :param command:
    :return:
    """
    splitted_path = command['path'].split('/')
    value = command['value']
    path_to_add = splitted_path[1]
    index_to_add = None
    if path_to_add not in document.keys():
        document[path_to_add] = value
        return document, ""
    if len(splitted_path) == 3:
        index_to_add = splitted_path[2]
        try:
            index_to_add = int(index_to_add)
        except ValueError:
            pass
        try:
            document[path_to_add][index_to_add]

        except (IndexError, KeyError):
            if not isinstance(index_to_add, int):
                document[path_to_add] = {index_to_add: value}
            else:
                try:
                    if isinstance(document[path_to_add], list):
                        document[path_to_add].insert(index_to_add, value)
                    elif isinstance(document[path_to_add], dict):
                        document[path_to_add][index_to_add].update(value)
                except ValueError:
                    return {}, "Incorrect structure to add."
        else:
            return {}, "Can't overwrite existing value."
    else:
        try:
            if isinstance(document[path_to_add], list):
                document[path_to_add].append(value)
            elif isinstance(document[path_to_add], dict):
                document[path_to_add].update(value)
        except ValueError:
            return {}, "Incorrect structure to add."
    return document, ""


def move(document, command):
    splitted_from_path = command['from'].split('/')
    splitted_to_path = command['path'].split('/')
    from_path = splitted_from_path[1]
    to_path = splitted_to_path[1]
    index_to_move_from = None

    if len(splitted_from_path) == 3:
        index_to_move_from = int(splitted_from_path[2])
    try:
        if index_to_move_from is None:
            value_to_move = document[from_path]
        else:
            value_to_move = document[from_path][index_to_move_from]
    except KeyError:
        return {}, "Can't move from not exist path."
    except IndexError:
        return {}, "Can't move not exist object."
    document[from_path] = []
    try:
        if type(value_to_move) == list:
            document[to_path].extend(value_to_move)
        else:
            document[to_path].append(value_to_move)
    except KeyError:
        return {}, "Can't move to not exist path."
    return document, ""


def replace(document, command):
    splitted_path = command['path'].split('/')
    path_to_replace = splitted_path[1]
    index_to_replace = None
    if len(splitted_path) == 3:
        index_to_replace = int(splitted_path[2])
    value = command['value']
    try:
        if index_to_replace is None:
            document[path_to_replace] = value
        else:
            document[path_to_replace][index_to_replace] = value
    except IndexError:
        return {}, "Can't replace not existing object."
    except KeyError:
        return {}, "Can't replace not existing path."
    return document, ""


def copy(document, command):
    splitted_path = command['from'].split('/')
    coppied_path = splitted_path[1]
    to_path = command['path'].split('/')[1]
    index_to_copy = None

    if len(splitted_path) == 3:
        try:
            index_to_copy = int(splitted_path[2])
        except ValueError:
            index_to_copy = splitted_path[2]
    try:
        if index_to_copy is None:
            value_to_copy = document[coppied_path]
        else:
            value_to_copy = document[coppied_path][index_to_copy]
    except KeyError:
        return {}, "Can't copy from not exist path."
    except IndexError:
        return {}, "Can't copy from not exist object."
    except TypeError:
        return {}, "Can't get key address from list."
    try:
        if type(value_to_copy) == list:
            document[to_path].extend(value_to_copy)
        else:
            document[to_path].append(value_to_copy)
    except KeyError:
        return {}, "Can't copy to not exist path."
    return document, ""


def test(document, command):
    splitted_path = command['path'].split('/')
    path = splitted_path[1]
    object_address = None
    expected_value = command['value']
    if len(splitted_path) == 3:
        object_address = splitted_path[2]
        try:
            object_address = int(object_address)
        except ValueError:
            object_address = object_address
    try:
        if object_address is None:
            tested_value = document[path]
        else:
            tested_value = document[path][object_address]
    except KeyError:
        return {}, "Can't test not exist path."
    except IndexError:
        return {}, "Can't test not exist object."

    if tested_value == expected_value:
        return document, ""
    return {}, "Test fail. Value is different than expected."


commands_functions = {"remove": remove,
                      "add": add,
                      "move": move,
                      "replace": replace,
                      "copy": copy,
                      "test": test}
