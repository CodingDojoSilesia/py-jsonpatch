from flask import Flask, send_from_directory, request
from flask.json import jsonify

from os import path, remove
from glob import glob

import json
import patch_lib

DIR = dir_path = path.dirname(path.realpath(__file__))
app = Flask(__name__)


def _get_pathfile(name):
    return path.join(DIR, 'files', name + '.json')


def _load_file(name):
    try:
        with open(_get_pathfile(name)) as fp:
            return json.load(fp)
    except FileNotFoundError:
        return jsonify(error='file not found'), 404
    except IOError:
        return jsonify(error='problem with read file'), 500
    except ValueError as exp:
        return jsonify(error=str(exp)), 500


def _write_file(name, data):
    with open(_get_pathfile(name), 'w') as fp:
        json.dump(data, fp)


def _remove_file(name):
    try:
        remove(_get_pathfile(name))
    except FileNotFoundError:
        return jsonify(error='file not found'), 404
    except IOError:
        return jsonify(error='problem with removing file'), 500
    else:
        return None


@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')


@app.route('/documents/', methods=['GET'])
def get_all_documents():
    files = glob(path.join(DIR, 'files', '*.json'))
    documents = [path.basename(filepath) for filepath in files]
    return jsonify(documents)


@app.route('/documents/<name>.json', methods=['GET'])
def get_document(name):
    data = _load_file(name)
    if isinstance(data, tuple):  # error
        return data

    return jsonify(data)


@app.route('/documents/<name>.json', methods=['PUT'])
def put_document(name):
    try:
        data = json.loads(request.data)
    except ValueError as exp:
        return jsonify(error=str(exp)), 400

    _write_file(name, data)
    return jsonify(data)


@app.route('/documents/<name>.json', methods=['PATCH'])
def patch_document(name):
    data = _load_file(name)
    if isinstance(data, tuple):  # error
        return data

    try:
        commands = json.loads(request.data)
    except ValueError as exp:
        return jsonify(error=str(exp)), 400

    try:
        new_data = patch_lib.patch_document(data, commands)
    except patch_lib.PatchError as exp:
        return jsonify(error=str(exp)), 400

    _write_file(name, new_data)
    return jsonify(new_data)


@app.route('/documents/<name>.json', methods=['DELETE'])
def delete_document(name):
    data = _remove_file(name)
    if isinstance(data, tuple):  # error
        return data

    return "", 204
