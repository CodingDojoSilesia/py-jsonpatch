from flask import Flask, render_template, request, abort
from flask.json import jsonify

from os import path
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


@app.route('/')
def index():
    files = glob(path.join(DIR, 'files', '*.json'))
    documents = [path.basename(filepath) for filepath in files]
    return render_template('index.html', documents=documents)


@app.route('/<name>.json', methods=['GET'])
def get_document(name):
    data = _load_file(name)
    if isinstance(data, tuple):  # error
        return data

    return jsonify(data)


@app.route('/<name>.json', methods=['PUT'])
def put_document(name):
    try:
        data = json.loads(request.data)
    except ValueError as exp:
        return jsonify(error=str(exp)), 400

    _write_file(name, data)
    return jsonify(data)


@app.route('/<name>.json', methods=['PATCH'])
def patch_document(name):
    data = _load_file(name)
    if isinstance(data, tuple):  # error
        return data

    try:
        commands = json.loads(request.data)
    except ValueError as exp:
        return jsonify(error=str(exp)), 400

    new_data = patch_lib.patch_document(data, commands)
    _write_file(name, new_data)
    return jsonify(new_data)

