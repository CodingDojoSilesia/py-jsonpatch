from copy import deepcopy


class PatchError(Exception):
    pass


def patch_document(document, commands):
    for command in commands:
        callback = CALLBACKS.get(command['op'])
        callback(document, command)
    return document


def add_callback(document, command, replace=False):
    path = command['path']
    value = deepcopy(command['value'])
    parent, key = find_parent_and_key_with_path(document, path)
    if key == '-':
        parent.append(value)
    else:
        if not replace and key in parent:
            raise PatchError(f'key exists in {path!r}')
        parent[key] = value


def remove_callback(document, command):
    path = command['path']
    parent, key = find_parent_and_key_with_path(document, path)

    del parent[key]


def replace_callback(document, command):
    add_callback(document, command, replace=True)


CALLBACKS = {
    'add': add_callback,
    'remove': remove_callback,
    'replace': replace_callback,
}


def find_parent_and_key_with_path(obj, path):
    return find_parent_and_key(obj, path_to_list(path))


def find_parent_and_key(obj, path_list):
    key, *new_path_list = path_list

    if isinstance(obj, list) and key != '-':
        key = int(key)

    if not new_path_list:
        return obj, key 

    try:
        nested_obj = obj[key]
    except (KeyError, IndexError, ValueError):
        raise PatchError(f"{key!r} doesn't exist")

    if not isinstance(nested_obj, dict) and not isinstance(nested_obj, list):
        type_name = type(nested_obj).__name__
        raise PatchError(f'{key!r} has a wrong nested type: {type_name}')

    return find_parent_and_key(nested_obj, new_path_list)


def path_to_list(path):
    if path[0] != '/':
        raise PatchError('wrong path')
    if len(path) == 1:
        return []
    return path[1:].split('/')
