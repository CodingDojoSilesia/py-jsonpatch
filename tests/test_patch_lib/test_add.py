from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_add_to_existing_path_list():
    add_command = {"op": "add", "path": "/hello/0", "value": "world"}
    document = patch_document({"hello": []}, [add_command])
    assert document == {"hello": ["world"]}


def test_add_to_list_index_when_without_value():
    add_command = {"op": "add", "path": "/hello/1", "value": ["world"]}
    document = patch_document({"hello": ["first"]}, [add_command])
    assert document == {"hello": ["first", ["world"]]}


def test_add_to_list_index_when_need_overwrite():
    add_command = {"op": "add", "path": "/hello/0", "value": ["world"]}
    old_document = {"hello": ["reserved"]}
    with raises(PatchError) as error:
        patch_document(old_document, [add_command])
    assert str(error.value) == "Can't overwrite existing value."


def test_add_to_dict_field():
    add_command = {"op": "add",
                   "path": "/hello/name",
                   "value": {'test': "test"}}
    old_document = {"hello": {'foo': 'poo'}}
    document = patch_document(old_document, [add_command])
    assert document == {"hello": {'name': {'test': "test"}, 'foo': 'poo'}}


def test_add_path():
    add_command = {"op": "add", "path": "/hello", "value": ["world"]}
    document = patch_document({}, [add_command])
    assert document == {"hello": ["world"]}


def test_add_list_to_path_with_dict():
    add_command = {"op": "add", "path": "/hello/list", "value": ["world"]}
    old_document = {"hello": {"name": "empty"}}

    document = patch_document(old_document, [add_command])
    assert document == {"hello": {"name": "empty", "list": ["world"]}}


def test_add_dict_to_path_with_list():
    add_command = {"op": "add", "path": "/hello/1", "value": {"name": "empty"}}
    old_document = {"hello": ["value"]}
    document = patch_document(old_document, [add_command])
    assert document == {"hello": ["value", {"name": "empty"}]}


def test_add_path_with_dict():
    add_command = {"op": "add", "path": "/hello", "value": {"name": "no name"}}
    document = patch_document({}, [add_command])
    assert document == {"hello": {"name": "no name"}}


def test_add_path_with_string():
    add_command = {"op": "add", "path": "/hello", "value": "name"}
    document = patch_document({}, [add_command])
    assert document == {"hello": "name"}
