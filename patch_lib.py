from logging import getLogger
logger = getLogger(__name__)


class PatchError(Exception):
    pass


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
    logger.error(commands)
    logger.info(commands)
    print(document)
    return document
    if "something_is_wrong":
        raise PatchError('something is wrong, dude')
