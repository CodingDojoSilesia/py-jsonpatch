from patch_lib import patch_document
from patch_lib import PatchError
from pytest import raises


def test_test_when_correct_value_dict_field():
    test_command = {"op": "test",
                    "path": "/best_biscuit/name",
                    "value": "Choco Leibniz"}
    old_document = {"best_biscuit": {'name': "Choco Leibniz"}}
    document = patch_document(old_document, [test_command])
    assert document == old_document


def test_test_when_correct_value_list_element():
    test_command = {"op": "test",
                    "path": "/best_biscuit/0",
                    "value": "Choco Leibniz"}
    old_document = {"best_biscuit": ["Choco Leibniz"]}
    document = patch_document(old_document, [test_command])
    assert document == old_document


def test_test_when_correct_list():
    test_command = {"op": "test",
                    "path": "/best_biscuit",
                    "value": ["Choco Leibniz", "foo"]}
    old_document = {"best_biscuit": ["Choco Leibniz", "foo"]}
    document = patch_document(old_document, [test_command])
    assert document == old_document


def test_test_when_correct_value_dict():
    test_command = {"op": "test",
                    "path": "/best_biscuit",
                    "value": {"name": "Choco Leibniz"}}
    old_document = {"best_biscuit": {"name": "Choco Leibniz"}}
    document = patch_document(old_document, [test_command])
    assert document == old_document


def test_test_when_value_not_exist():
    test_command = {"op": "test",
                    "path": "/best_biscuit/name",
                    "value": "Choco Leibniz"}
    with raises(PatchError) as error:
        patch_document(
            {"best_biscuit": {'name': "Choko sticker"}
             }, [test_command])
    assert str(error.value) == "Test fail. Value is different than expected."


def test_test_when_path_not_exist():
    test_command = {"op": "test",
                    "path": "/fooo/name",
                    "value": "Choco Leibniz"}
    with raises(PatchError) as error:
        patch_document(
            {"best_biscuit": {'name': "Choko sticker"}
             }, [test_command])
    assert str(error.value) == "Can't test not exist path."


def test_test_when_object_address_not_exist():
    test_command = {"op": "test",
                    "path": "/fooo/name",
                    "value": "Choco Leibniz"}
    with raises(PatchError) as error:
        patch_document(
            {"best_biscuit": {'name': "Choko sticker"}
             }, [test_command])
    assert str(error.value) == "Can't test not exist path."


def test_test_when_object_index_object_out_of_range():
    test_command = {"op": "test",
                    "path": "/fooo/1",
                    "value": "Choco Leibniz"}
    with raises(PatchError) as error:
        patch_document(
            {"best_biscuit": ["first"]
             }, [test_command])
    assert str(error.value) == "Can't test not exist path."
