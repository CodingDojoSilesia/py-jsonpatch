# py-jsonpatch

## Mission
support http://jsonpatch.com/ in `patch_lib.py`

And of course, write tests in `tests/test_patch_lib.py`

## Protips
* Treat JSON like a tree structure
* JSONPatch syntax is always valid
* …but path to document can be invalid (not exist or syntax error)
* don't move/modify root (`/`) - it's an insane!
* when commands 'add' and 'remove' will be implemented then other commands would be very easy to implement


## How to run

### Pipenv
#### Install

```
pipenv install --three
```
#### Run tests
```
pipenv run tests
```
#### Run web console
```
pipenv run web
```

### with virtualenv
#### Install

```
virtualenv venv -ppython3
source venv/bin/activate
pip install flask pytest pytest-cov flake8
pipenv install --three
```
#### Run tests
```
flake8 && pytest -v --cov=.
```
#### Run web console
```
FLASK_APP=web flask run
```
