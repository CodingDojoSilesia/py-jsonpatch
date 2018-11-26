from helpers import get_path_elements_as_list
from helpers import is_path_exist
from helpers import add_value_by_path
from helpers import replace_value_by_path
from helpers import remove_by_path
from helpers import get_value_by_path

def remove(document, command):
    """
    Remove path.
    :param document: dict
    :param command: dict example: {"op": "remove", "path": "/test"}
    :return:
    """
    elements = get_path_elements_as_list(command['path'])
    if not is_path_exist(document, *elements):
        return {}, f"Can't remove not exist object: {elements[-1]}."
    path_to_remove = "][".join(repr(n) for n in elements)
    exec(f"del document[{path_to_remove}]")  # bad practice
    return document, ""


def add(document, command):
    """
    Adds a value to an object or inserts it into an array.
    :param document: dict
    :param command: dict {"op": "add", "path": "/hello", "value": ["world"]}
    :return: tuple( document(dict), error(str))
    """
    elements = get_path_elements_as_list(command['path'])

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


def move(document, command):
    """
    Move value from path to path.
    :param document: dict
    :param command: dict example :
    {"op": "move", "from": "/biscuits/0", "path": "/cookies/2"}
    :return: (document(dict), error(str))
    """
    elements_path_from = get_path_elements_as_list(command['from'])
    elements_to_path = get_path_elements_as_list(command['path'])

    if not is_path_exist(document, *elements_path_from):
        return {}, "Can't move from not exist path."

    value_to_move = remove_by_path(document, elements_path_from)
    try:
        add_value_by_path(document, elements_to_path, value_to_move)
    except AttributeError:
        return {}, "Wrong type to add"
    except KeyError:
        return {}, "Can't move to not exist path."
    return document, ""


def replace(document, command):
    path_to_replace = get_path_elements_as_list(command['path'])
    value = command['value']
    if not is_path_exist(document, *path_to_replace):
        return {}, "Can't replace not existing path."
    replace_value_by_path(document, path_to_replace, value)
    return document, ""


def copy(document, command):
    """
    Copy value from path to path.
    :param document: dict
    :param command: dict example :
    {"op": "copy", "from": "/biscuits/0", "path": "/cookies/2"}
    :return: (document(dict), error(str))
    """
    elements_path_from = get_path_elements_as_list(command['from'])
    elements_to_path = get_path_elements_as_list(command['path'])

    if not is_path_exist(document, *elements_path_from):
        return {}, "Can't copy from not exist path."

    value_to_copy = get_value_by_path(document, elements_path_from)
    try:
        add_value_by_path(document, elements_to_path, value_to_copy)
    except AttributeError:
        return {}, "Wrong type to add"
    except KeyError:
        return {}, "Can't copy to not exist path."
    return document, ""


def test(document, command):
    """
    Check is path has expected value.
    :param document: dict
    :param command: dict example:
     {"op": "test", "path": "/fooo/1", "value": "Choco Leibniz"}
    :return: (document(dict), error(str))
    """
    path_elements = get_path_elements_as_list(command['path'])
    expected_value = command['value']
    if not is_path_exist(document, *path_elements):
        return {}, "Can't test not exist path."
    actual_value = get_value_by_path(document, path_elements)
    if actual_value == expected_value:
        return document, ""
    return {}, "Test fail. Value is different than expected."


commands_functions = {"remove": remove,
                      "add": add,
                      "move": move,
                      "replace": replace,
                      "copy": copy,
                      "test": test}
