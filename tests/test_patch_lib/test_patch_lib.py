from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_not_modified_document():
    document = patch_document({"test": "test"}, [])
    assert document == {"test": "test"}


def test_not_known_command():
    command = {"op": "fooo", "path": "/test"}
    with raises(PatchError) as error:
        patch_document({"hello": {}}, [command])
    assert str(error.value) == "Not known command:fooo"
