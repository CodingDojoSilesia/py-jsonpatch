from copy import deepcopy


class PatchError(Exception):
    pass


def patch_document(document, commands):
    for command in commands:
        callback = CALLBACKS.get(command['op'])
        callback(document, command)
    return document


def add_callback(document, command):
    path = command['path']
    value = deepcopy(command['value'])
    parent, key = find_parent_and_key_with_path(document, path)
    if key == '-':
        parent.append(value)
    else:
        raise_if_found(parent, key, path)
        parent[key] = value


def remove_callback(document, command):
    path = command['path']
    parent, key = find_parent_and_key_with_path(document, path)
    raise_if_not_found(parent, key, path)
    del parent[key]


def replace_callback(document, command):
    path = command['path']
    value = deepcopy(command['value'])
    parent, key = find_parent_and_key_with_path(document, path)
    raise_if_not_found(parent, key, path)
    parent[key] = value


def move_callback(document, command, copy=False):
    from_path = command['from']
    from_parent, from_key = find_parent_and_key_with_path(document, from_path)
    raise_if_not_found(from_parent, from_key, from_path)

    add_callback(
        document=document,
        command={
            'path': command['path'],
            'value': from_parent[from_key],
        }
    )

    if not copy:
        del from_parent[from_key]


def test_callback(document, command):
    path = command['path']
    value = command['value']
    parent, key = find_parent_and_key_with_path(document, path)
    raise_if_not_found(parent, key, path)

    if parent[key] != value:
        raise PatchError(f'test in {path!r} has failed')


def raise_if_not_found(parent, key, path):
    try:
        parent[key]
    except (IndexError, KeyError):
        raise PatchError(f'key doesn\'t exist in {path!r}')


def raise_if_found(parent, key, path):
    try:
        parent[key]
    except (IndexError, KeyError):
        pass
    else:
        raise PatchError(f'key exists in {path!r}')


CALLBACKS = {
    'add': add_callback,
    'remove': remove_callback,
    'replace': replace_callback,
    'move': move_callback,
    'copy': lambda d, c: move_callback(d, c, copy=True),
    'test': test_callback,
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
    if path[0] != '/' or len(path) == 1:
        raise PatchError('wrong path')
    return path[1:].split('/')
