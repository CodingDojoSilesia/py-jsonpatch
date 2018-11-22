from commands import commands_functions


class PatchError(Exception):
    pass


def execute_properly_modification(document, command):
    try:
        make_changes = commands_functions[command['op']]
    except KeyError as error:
        return {}, f"Not known command:{error.args[0]}"
    return make_changes(document, command)


def patch_document(document, commands):
    """
    Modify document with commands.

    :param document: dict with actual document
    :param commands: list with dicts of commands
    example:
    [{"op": "remove", "path": "/fooo"},
    {"op": "add", "path": "/hello", "value": ["world"]},
    {"op": "move", "from": "/biscuits", "path": "/cookies"}]
    :return: dict with updated document by received commands
    """
    new_doc = document.copy()
    for command in commands:
        new_doc, error = execute_properly_modification(new_doc, command)
        if error:
            raise PatchError(error)
    return new_doc
