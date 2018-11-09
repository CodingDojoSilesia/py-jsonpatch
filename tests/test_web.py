from web import app
from unittest.mock import patch

import pytest

patch_load_file = patch('web._load_file')
patch_write_file = patch('web._write_file')
patch_lib = patch('web.patch_lib')


@pytest.fixture
def client():
    yield app.test_client()


@patch_load_file
def test_get_document(load_file, client):
    load_file.return_value = {'test': 'test'}
    response = client.get('documents/test.json')

    assert response.status == '200 OK'
    assert response.data == b'{"test":"test"}\n'
    assert response.content_type == 'application/json'
    load_file.assert_called_once_with('test')


@patch_write_file
def test_put_document(write_file, client):
    response = client.put('documents/test.json', json={'new': 'new'})

    assert response.status == '200 OK'
    assert response.data == b'{"new":"new"}\n'
    assert response.content_type == 'application/json'
    write_file.assert_called_once_with('test', {'new': 'new'})


@patch_write_file
@patch_load_file
@patch_lib
def test_patch_document(patch_lib, load_file, write_file, client):
    old_document = {'test': 'test'}
    new_document = {'new': 'new'}
    load_file.return_value = old_document
    patch_lib.patch_document.return_value = new_document

    commands = [
        {'op': 'add', 'path': '/new', 'value': 'new'},
        {'op': 'remove', 'path': '/test'},
    ]
    response = client.patch('documents/test.json', json=commands)

    assert response.status == '200 OK'
    assert response.data == b'{"new":"new"}\n'
    assert response.content_type == 'application/json'
    load_file.assert_called_once_with('test')
    write_file.assert_called_once_with('test', new_document)
    patch_lib.patch_document.assert_called_once_with(old_document, commands)
