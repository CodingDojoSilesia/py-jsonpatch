from patch_lib import patch_document, find_parent_and_key, path_to_list
from patch_lib import PatchError

import pytest


def test_not_modified_document():
    document = patch_document({"test": "test"}, [])
    assert document == {"test": "test"}


def test_add_value():
    result = patch_document(
        document={},
        commands=[
            {'op': 'add', 'path': '/foobar', 'value': 'alabama'},
        ],
    )
    assert result == {'foobar': 'alabama'}


def test_add_value_nested():
    result = patch_document(
        document={},
        commands=[
            {'op': 'add', 'path': '/foo', 'value': {}},
            {'op': 'add', 'path': '/foo/bar', 'value': 'alabama'},
        ],
    )
    assert result == {
        'foo': {'bar': 'alabama'}
    }


def test_add_value_to_list():
    result = patch_document(
        document={},
        commands=[
            {'op': 'add', 'path': '/foo', 'value': []},
            {'op': 'add', 'path': '/foo/-', 'value': 'first'},
            {'op': 'add', 'path': '/foo/-', 'value': 'second'},
            {'op': 'add', 'path': '/foo/0', 'value': 'third'},
        ],
    )
    assert result == {
        'foo': ['third', 'second'],
    }


def test_remove_value_to_list():
    result = patch_document(
        document={
            'dict': {'foo': 'bar'},
            'dict-to-remove': {'foo': 'bar'},
            'list': [1, 2, 3],
            'list-to-remove': [1, 2, 3],
            'foo': 'bar',
        },
        commands=[
            {'op': 'remove', 'path': '/dict-to-remove'},
            {'op': 'remove', 'path': '/dict/foo'},
            {'op': 'remove', 'path': '/list-to-remove'},
            {'op': 'remove', 'path': '/list/1'},
            {'op': 'remove', 'path': '/foo'},
        ],
    )
    assert result == {
        'dict': {},
        'list': [1, 3],
    }


def test_add_value_in_exist_key():
    with pytest.raises(PatchError) as exinfo:
        patch_document(
            document={'foo': 'bar'},
            commands=[{'op': 'add', 'path': '/foo', 'value': 'xxx'}],
        )

    assert exinfo.value.args[0] == "key exists in '/foo'"


def test_replace_value():
    result = patch_document(
        document={
            'foo': 'bar',
            'list': ['foo'],
            'dict': {'foo': 'bar'},
        },
        commands=[
            {'op': 'replace', 'path': '/foo', 'value': 'xxx'},
            {'op': 'replace', 'path': '/list/0', 'value': 'xxx'},
            {'op': 'replace', 'path': '/dict/foo', 'value': 'xxx'},
        ],
    )

    assert result == {
        'foo': 'xxx',
        'list': ['xxx'],
        'dict': {'foo': 'xxx'},
    }


def test_replace_not_exist_key():
    with pytest.raises(PatchError) as excinfo:
        result = patch_document(
            document={'foo': 'bar'},
            commands=[{'op': 'replace', 'path': '/bar', 'value': 'xxx'}],
        )

    assert excinfo.value.args[0] == "key doesn't exist in '/bar'"


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


@pytest.mark.parametrize('path,result', [
    ('/', []),
    ('/foo', ['foo']),
    ('/foo/bar', ['foo', 'bar']),
    ('/foo/bar/1/-', ['foo', 'bar', '1', '-']),
    ('/foo//bar', ['foo', '', 'bar']),
    ('/foo/bar/', ['foo', 'bar', '']),
])
def test_path_to_list(path, result):
    assert path_to_list(path) == result


@pytest.mark.parametrize('wrong_path', [
    'bar',
])
def test_path_to_list__wrong(wrong_path):
    with pytest.raises(PatchError) as excinfo:
        path_to_list(wrong_path)

    assert excinfo.value.args[0] == 'wrong path'
