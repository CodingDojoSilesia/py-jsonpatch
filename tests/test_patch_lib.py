from patch_lib import patch_document


def test_not_modified_document():
    document = patch_document({"test": "test"}, [])
    assert document == {"test": "test"}
