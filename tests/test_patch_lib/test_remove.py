from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_remove():
    delete_command = {"op": "remove", "path": "/test"}
    document = patch_document({"test": "test"}, [delete_command])
    assert document == {}


def test_remove_not_exist_element():
    delete_command = {"op": "remove", "path": "/fooo"}
    with raises(PatchError) as error:
        patch_document({"test": "test"}, [delete_command])
    assert str(error.value) == "Can't remove not exist object: fooo."
