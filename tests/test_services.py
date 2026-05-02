from services.input_service import validate_item

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

def test_get_item_by_key():
    assert len(validate_item("item1", dictionary)) > 0

def test_get_item_by_malformed_key():
    assert len(validate_item("i T-em   -1", dictionary)) > 0
    assert len(validate_item("Some Long-item Name", dictionary)) > 0

def test_get_item_by_keyword():
    assert len(validate_item("alias", dictionary)) > 0
    assert len(validate_item("foo", dictionary)) > 0
    assert len(validate_item("bar", dictionary)) > 0
