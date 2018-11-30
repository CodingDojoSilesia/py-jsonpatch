from copy import deepcopy


class PatchError(Exception):
    pass


def patch_document(document, commands):
    for cmd in commands:
        execute_command(document, cmd)
    return document


def execute_command(document, command):
    path = command['path'].split('/')
    if not path[0] == '':
        raise PatchError('wrong path xd!')
    from_path = command.get('from', '').split('/')
    action = actions.get(command['op'])
    action(path, document, command.get('value') or from_path)
    return document


def replace(path, document, value):
    path.pop(0)
    char = path[0]
    if document.get(char) is None:
        raise PatchError('wrong path xd!')
    if len(path) > 1:
        if not isinstance(document[char], dict):
            raise PatchError('wrong path xd!')
        return replace(path, document[char], value)
    else:
        document[path[0]] = value


def add(path, document, value):
    path.pop(0)
    char = path[0]
    if document.get(char) is None:
        document[char] = {}
    if not isinstance(document[char], dict):
        raise PatchError('wrong path xd!')
    if len(path) > 1:
        return add(path, document[char], value)
    else:
        document[path[0]] = value


def remove(path, document, value):
    path.pop(0)
    char = path[0]
    if document.get(char) is None:
        raise PatchError('wrong path xd!')
    if len(path) > 1:
        if not isinstance(document[char], dict):
            raise PatchError('wrong path xd!')
        return remove(path, document[char], value)
    else:
        del (document[path[0]])


def test(path, document, value):
    val = get_val(path, document)
    if val != value:
        raise PatchError('didnt passt testes xddd')


def copy(path, document, value):
    val = get_val(value, document)
    try:
        add(path, document, val)
    except PatchError:
        replace(path, document, val)


def move(path, document, value):
    from_path = deepcopy(value)
    val = get_val(value, document)
    remove(from_path, document, '')
    try:
        add(path, document, val)
    except PatchError:
        replace(path, document, val)


def get_val(path, document):
    path.pop(0)
    char = path[0]
    if len(path) > 1:
        if not isinstance(document[char], dict):
            raise PatchError('wrong path xd')
        return get_val(path, document[char])
    else:
        return document[char]


actions = {
    'replace': replace,
    'add': add,
    'remove': remove,
    'test': test,
    'copy': copy,
    'move': move,
}
