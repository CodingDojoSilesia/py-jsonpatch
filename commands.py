def get_path_elements(path_to_split):
    splitted_path = path_to_split.split('/')
    path_elements = filter(str.strip, splitted_path)
    serialized_path = []
    for element in path_elements:
        try:
            serialized_path.append(int(element))
        except ValueError:
            serialized_path.append(element)
    return serialized_path


def remove(document, command):
    elements = get_path_elements(command['path'])
    if not is_path_exist(document, *elements):
        return {}, f"Can't remove not exist object: {elements[-1]}."
    path_to_remove = "][".join(repr(n) for n in elements)
    exec(f"del document[{path_to_remove}]")  # bad practice
    return document, ""


def add(document, command):
    """
    Adds a value to an object or inserts it into an array.
    :param document: dict
    :param command: str
    :return: tuple( document(dict), error(str))
    """
    elements = get_path_elements(command['path'])

    value = command['value']
    if is_path_exist(document, *elements):
        return {}, "Can't overwrite existing value."

    try:
        path_to_add = "][".join(repr(n) for n in elements)
        exec(f"document[{path_to_add}].update(value)")  # bad practice
    except KeyError:
        exec(f"document[{path_to_add}] = value")  # bad practice
    except IndexError:
        index = elements.pop(-1)
        path_to_add = "][".join(repr(n) for n in elements)
        exec(f"document[{path_to_add}].insert({index}, value)")  # bad practice
    return document, ""

def get_object_index(splitted_path):
    index = None
    if len(splitted_path) == 3:
        try:
            index = int(splitted_path[2])
        except (ValueError, TypeError):
            index = splitted_path[2]
    return index


def remove_by_path(data, keys):
    if len(keys) == 1:
        value = data[keys[0]]
        print(value)
        del data[keys[0]]
        return value
    return remove_by_path(data[keys[0]], keys[1:])

def add_value_by_path(data, keys, value_to_add):
    if len(keys) == 1:
        if type(data) == list:
            data.insert(keys[0], value_to_add)
        else:
            data[keys[0]].append(value_to_add)
        return True
    remove_by_path(data[keys[0]], keys[1:], value_to_add)

def move(document, command):
    elements_path_from = get_path_elements(command['from'])
    elements_to_path = get_path_elements(command['path'])

    if not is_path_exist(document, *elements_path_from):
        return {}, "Can't move from not exist path."
    if not is_path_exist(document, *elements_to_path):
        return {}, "Can't move to not exist path."
    value_to_move = remove_by_path(document, elements_path_from)
    print(value_to_move,'hh')
    add_value_by_path(document, elements_to_path, value_to_move)
    return document, ""

def is_path_exist(document, *args):
    try:
        doc_reference = document.copy()
        for i in args:
            doc_reference = doc_reference[i]
    except (IndexError, KeyError, TypeError) as e:
        print(e)
        return False
    return True


def replace(document, command):
    splitted_path = command['path'].split('/')
    path_to_replace = splitted_path[1]
    index_to_replace = get_object_index(splitted_path)
    value = command['value']
    if index_to_replace is None:
        if is_path_exist(document, path_to_replace):
            document[path_to_replace] = value
        else:
            return {}, "Can't replace not existing path."
    else:
        if is_path_exist(document, path_to_replace, index_to_replace):
            document[path_to_replace][index_to_replace] = value
        else:
            return {}, "Can't replace not existing path."

    return document, ""


def copy(document, command):
    splitted_path = command['from'].split('/')
    coppied_path = splitted_path[1]
    to_path = command['path'].split('/')[1]

    index_to_copy = get_object_index(splitted_path)

    if index_to_copy is None:
        if not is_path_exist(document, coppied_path):
            return {}, "Can't copy from not exist path."
        value_to_copy = document[coppied_path]
    else:
        if not is_path_exist(document, coppied_path, index_to_copy):
            return {}, "Can't copy from not exist path."
        value_to_copy = document[coppied_path][index_to_copy]
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
    expected_value = command['value']
    object_address = get_object_index(splitted_path)

    if object_address is None:
        if not is_path_exist(document, path):
            return {}, "Can't test not exist path."
        tested_value = document[path]
    else:
        if not is_path_exist(document, path, object_address):
            return {}, "Can't test not exist path."
        tested_value = document[path][object_address]

    if tested_value == expected_value:
        return document, ""
    return {}, "Test fail. Value is different than expected."


commands_functions = {"remove": remove,
                      "add": add,
                      "move": move,
                      "replace": replace,
                      "copy": copy,
                      "test": test}
