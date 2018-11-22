from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_replace_single_value():
    replace_command = {"op": "replace", "path": "/baz/0", "value": "boo"}
    old_document = {"baz": ["previous", "stay"]}
    document = patch_document(old_document, [replace_command])
    assert document == {"baz": ["boo", "stay"]}


def test_replace_list():
    replace_command = {"op": "replace", "path": "/baz", "value": "boo"}
    old_document = {"baz": ["ojoj", "stay"]}
    document = patch_document(old_document, [replace_command])
    assert document == {"baz": "boo"}


def test_replace_out_of_range():
    replace_command = {"op": "replace", "path": "/baz/5", "value": "boo"}
    old_document = {"baz": ["ojoj"]}
    with raises(PatchError) as error:
        patch_document(old_document, [replace_command])
    assert str(error.value) == "Can't replace not existing object."


def test_replace_not_exist_object():
    replace_command = {"op": "replace", "path": "/foo/5", "value": "boo"}
    old_document = {"baz": ["ojoj"]}
    with raises(PatchError) as error:
        patch_document(old_document, [replace_command])
    assert str(error.value) == "Can't replace not existing path."
