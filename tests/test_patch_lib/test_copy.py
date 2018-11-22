from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_copy_single_value_to_list():
    copy_command = {"op": "copy", "from": "/biscuits/0", "path": "/cookies"}
    old_document = {"biscuits": ["to_copy", "not_copy"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["to_copy", "not_copy"],
                        "cookies": ["cookie", "to_copy"]}


def test_copy_value_from_dict():
    copy_command = {"op": "copy", "from": "/biscuits/name", "path": "/cookies"}
    old_document = {"biscuits": {"name": "best"}, "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": {"name": "best"},
                        "cookies": ["cookie", "best"]}


def test_copy_list_to_list():
    copy_command = {"op": "copy", "from": "/biscuits", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit", "to_copy"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["biscuit", "to_copy"],
                        "cookies": ["cookie", "biscuit", "to_copy"]}


def test_copy_dict_to_list():
    copy_command = {"op": "copy", "from": "/biscuits", "path": "/cookies"}
    old_document = {"biscuits": {"name": "choko"}, "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": {"name": "choko"},
                        "cookies": ["cookie", {"name": "choko"}]}


def test_copy_not_exist_index():
    copy_command = {"op": "copy", "from": "/biscuits/1", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": []}
    with raises(PatchError) as error:
        patch_document(old_document, [copy_command])
    assert str(error.value) == "Can't copy from not exist object."


def test_copy_key_from_list():
    copy_command = {"op": "copy", "from": "/biscuits/name", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": []}
    with raises(PatchError) as error:
        patch_document(old_document, [copy_command])
    assert str(error.value) == "Can't get key address from list."


def test_copy_index_from_dict():
    copy_command = {"op": "copy", "from": "/biscuits/0", "path": "/cookies"}
    old_document = {"biscuits": {"name": "choko"}, "cookies": []}
    with raises(PatchError) as error:
        patch_document(old_document, [copy_command])
    assert str(error.value) == "Can't copy from not exist path."
