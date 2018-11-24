from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_remove_list_element():
    delete_command = {"op": "remove", "path": "/foo/0"}
    document = patch_document({"foo": [1, 2]}, [delete_command])
    assert document == {'foo': [2]}


def test_remove():
    delete_command = {"op": "remove", "path": "/test"}
    document = patch_document({"test": "test"}, [delete_command])
    assert document == {}


def test_remove_not_exist_element():
    delete_command = {"op": "remove", "path": "/fooo"}
    with raises(PatchError) as error:
        patch_document({"test": "test"}, [delete_command])
    assert str(error.value) == "Can't remove not exist object: fooo."


def test_remove_nested_dict_key():
    delete_command = {"op": "remove", "path": "/foo/name"}
    new_document = patch_document(
        {"foo": {"name": "anna", "eyes": "black"}}, [delete_command])
    assert new_document == {"foo": {"eyes": "black"}}
