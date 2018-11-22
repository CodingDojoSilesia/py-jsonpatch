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


def test_not_known_command():
    command = {"op": "fooo", "path": "/test"}
    with raises(PatchError) as error:
        patch_document({"hello": {}}, [command])
    assert str(error.value) == "Not known command:fooo"


def test_remove_not_exist_element():
    delete_command = {"op": "remove", "path": "/fooo"}
    with raises(PatchError) as error:
        patch_document({"test": "test"}, [delete_command])
    assert str(error.value) == "Can't remove not exist object: fooo."


def test_add_existing_path():
    add_command = {"op": "add", "path": "/hello", "value": ["world"]}
    with raises(PatchError) as error:
        patch_document({"hello": {}}, [add_command])
    assert str(error.value) == "Can't add existing path."


def test_add():
    add_command = {"op": "add", "path": "/hello", "value": ["world"]}
    document = patch_document({}, [add_command])
    assert document == {"hello": ["world"]}


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


def test_move_path_list():
    move_command = {"op": "move", "from": "/biscuits", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": ["cookie"]}
    document = patch_document(old_document, [move_command])
    assert document == {"biscuits": [], "cookies": ["cookie", "biscuit"]}


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


def test_copy_single_value_to_list():
    copy_command = {"op": "copy", "from": "/biscuits/0", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit", "not_copy"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["biscuit", "not_copy"],
                        "cookies": ["cookie", "biscuit"]}


def test_copy_value_to_end_of_list():
    copy_command = {"op": "copy", "from": "/biscuits/0", "path": "/cookies/-"}
    old_document = {"biscuits": ["biscuit", "not_copy"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["biscuit", "not_copy"],
                        "cookies": ["cookie", "biscuit"]}


def test_copy_list_to_list():
    copy_command = {"op": "copy", "from": "/biscuits", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit", "to_copy"], "cookies": ["cookie"]}
    document = patch_document(old_document, [copy_command])
    assert document == {"biscuits": ["biscuit", "to_copy"],
                        "cookies": ["cookie", "biscuit", "to_copy"]}


def test_move_not_exist_element():
    copy_command = {"op": "move", "from": "/biscuits/1", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": []}
    with raises(PatchError) as error:
        patch_document(old_document, [copy_command])
    assert str(error.value) == "Can't move not exist object."


def test_copy_not_exist_element():
    copy_command = {"op": "copy", "from": "/biscuits/1", "path": "/cookies"}
    old_document = {"biscuits": ["biscuit"], "cookies": []}
    with raises(PatchError) as error:
        patch_document(old_document, [copy_command])
    assert str(error.value) == "Can't copy from not exist object."


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
    with raises(PatchError) as error:
        patch_document(
            {"best_biscuit": {'name': "Choko sticker"}
             }, [test_command])
    assert str(error.value) == "Test fail. Value is different than expected."
