from services.input_service import transform_string, validate_item

dictionary = {
    "item1": {
        "name": "Item Name",
        "keywords": ["alias"]
    },
    "somelongitemname": {
        "name": "Hello, World!",
        "keywords": ["foo", "bar"]
    }
}

def test_validate_item_by_key():
    assert len(validate_item("item1", dictionary)) > 0

def test_validate_item_by_keyword():
    assert len(validate_item("alias", dictionary)) > 0
    assert len(validate_item("foo", dictionary)) > 0
    assert len(validate_item("bar", dictionary)) > 0

def test_invalid_item():
    assert len(validate_item("pootis", dictionary)) == 0

def test_transform_string():
    assert transform_string("ThIS   is-A-   - weird ST rIN-g  ") \
        == "thisisaweirdstring"