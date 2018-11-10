class PatchError(Exception):
    pass


def patch_document(document, commands):
    return document
    if "something_is_wrong":
        raise PatchError('something is wrong, dude')
