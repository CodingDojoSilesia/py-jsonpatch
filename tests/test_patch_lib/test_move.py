from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_move_single_value():
    move_command = {"op": "move", "from": "/biscuits/0", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit", "second"], "cookies": ["cookie"]}
    document = patch_document(old_document, [move_command])
    assert document == {"biscuits": [], "cookies": ["cookie", "biscuit"]}


def test_move_from_not_exist_path():
    move_command = {"op": "move", "from": "/foo", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    with raises(PatchError) as error:
        patch_document(old_document, [move_command])
    assert str(error.value) == "Can't move from not exist path."


def test_move_to_not_exist_path():
    move_command = {"op": "move", "from": "/biscuits", "path": "/foo"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    with raises(PatchError) as error:
        patch_document(old_document, [move_command])
    assert str(error.value) == "Can't move to not exist path."


def test_move_not_exist_element():
    copy_command = {"op": "move", "from": "/biscuits/1", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": []}
    with raises(PatchError) as error:
        patch_document(old_document, [copy_command])
    assert str(error.value) == "Can't move from not exist path."
