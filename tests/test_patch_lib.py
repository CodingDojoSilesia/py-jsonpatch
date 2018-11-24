from patch_lib import patch_document, find_parent_and_key, PatchError

import pytest


def test_not_modified_document():
    document = patch_document({"test": "test"}, [])
    assert document == {"test": "test"}


def test_find_parent_and_key_flat():
    obj = {'key': 'foobar'}
    parent, key = find_parent_and_key(obj,  ['key'])

    assert parent is obj
    assert key == 'key'


def test_find_parent_and_key_nested_dict():
    obj = {
        'nested': {'key': 'foobar'}
    }
    parent, key = find_parent_and_key(obj,  ['nested', 'key'])

    assert parent is obj['nested']
    assert key == 'key'


def test_find_parent_and_key_nested_dict_and_numeric_key():
    obj = {
        '123': {'key': 'foobar'}
    }
    parent, key = find_parent_and_key(obj,  ['123', 'key'])

    assert parent is obj['123']
    assert key == 'key'


def test_find_parent_and_key_nested_list():
    obj = {
        'list': [
            ['marek', 'foobar'],
        ]
    }
    parent, key = find_parent_and_key(obj,  ['list', '0', '1'])

    assert parent is obj['list'][0]
    assert key == 1


def test_find_parent_and_key_wrong_nested():
    obj = {
        'wrong_key': 'foobar'
    }

    with pytest.raises(PatchError) as exc:
        parent, key = find_parent_and_key(obj,  ['wrong_key', 'value'])

    assert exc.value.args[0] == "'wrong_key' has a wrong nested type: str"


def test_find_parent_and_key_not_exist():
    obj = {}

    with pytest.raises(PatchError) as exc:
        parent, key = find_parent_and_key(obj,  ['not_exist', 'foo'])

    assert exc.value.args[0] == "'not_exist' doesn't exist"
