class PatchError(Exception):
    pass


def patch_document(document, commands):
    return document
    if "something_is_wrong":
        raise PatchError('something is wrong, dude')


def find_parent_and_key(obj, path_list):
    key, *new_path_list = path_list

    if isinstance(obj, list):
        key = int(key)

    if not new_path_list:
        return obj, key 

    try:
        nested_obj = obj[key]
    except (KeyError, IndexError):
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
