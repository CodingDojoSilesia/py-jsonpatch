from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_not_modified_document():
    document = patch_document({"test": "test"}, [])
    assert document == {"test": "test"}


def test_remove():
    delete_command = {"op": "remove", "path": "/test"}
    document = patch_document({"test": "test"}, [delete_command])
    assert document == {}


def test_remove_not_exist_element():
    delete_command = {"op": "remove", "path": "/fooo"}
    with raises(PatchError):
        patch_document({"test": "test"}, [delete_command])


def test_add_existing_path():
    add_command = {"op": "add", "path": "/hello", "value": ["world"]}
    with raises(PatchError):
        patch_document({"hello": {}}, [add_command])


def test_add():
    add_command = {"op": "add", "path": "/hello", "value": ["world"]}
    document = patch_document({}, [add_command])
    assert document == {"hello": ["world"]}


def test_replace():
    replace_command = {"op": "replace", "path": "/baz/1", "value": "boo"}
    old_document = {"baz": ["ojoj"]}
    document = patch_document(old_document, [replace_command])
    assert document == {"baz": ["boo"]}


def test_move_path_list():
    move_command = {"op": "move", "from": "/biscuits", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    document = patch_document(old_document, [move_command])
    assert document == {"biscuits": [], "cookies": ["cookie", "biscuit"]}


def test_move_not_exist_element():
    move_command = {"op": "move", "from": "/biscuits", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    with raises(PatchError):
        patch_document(old_document, [move_command])


def test_copy_value_to_list():
    copy_command = {"op": "copy", "from": "/biscuits/0", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["biscuit"],
                        "cookies": ["biscuit", "cookie"]}


def test_copy_value_to_end_of_list():
    copy_command = {"op": "copy", "from": "/biscuits/0", "path": "/cookies/-"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["biscuit"],
                        "cookies": ["cookie", "biscuit", ]}


def test_copy_list_to_list():
    copy_command = {"op": "copy", "from": "/biscuits", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["biscuit"],
                        "cookies": ["cookie", "biscuit"]}


def test_copy_not_exist_element():
    copy_command = {"op": "move", "from": "/biscuits/1", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": {}}
    with raises(PatchError):
        patch_document(old_document, [copy_command])


def test_test_when_value_exist():
    test_command = {"op": "test",
                    "path": "/best_biscuit/name",
                    "value": "Choco Leibniz"}
    old_document = {"best_biscuit": {'name': "Choco Leibniz"}}
    document = patch_document(old_document, [test_command])
    assert document == {"best_biscuit": {'name': "Choco Leibniz"}}


def test_test_when_value_not_exist():
    test_command = {"op": "test",
                    "path": "/best_biscuit/name",
                    "value": "Choco Leibniz"}
    with raises(PatchError):
        patch_document(
            {"best_biscuit": {'name': "Choko sticker"}}, [test_command])
