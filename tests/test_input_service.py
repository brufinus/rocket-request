from services.input_service import get_similar_item, transform_string, \
    validate_item

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

def test_get_similar_item():
    assert get_similar_item("item", dictionary) == "item1"
    thisdict = {"grapple": "0.73", "orange": "0.4", "apple": "0.89"}
    assert get_similar_item("aple", thisdict) == "apple"

def test_get_with_confidence():
    # Returns sword as it's above the confidence threshold.
    thisdict = {"sword": "0.89", "word": "1.0"}
    assert get_similar_item("word", thisdict) == "sword"

def test_no_similar_items():
    assert get_similar_item("banana", dictionary) == ""

def test_get_similar_items_no_item():
    assert get_similar_item("", dictionary) == ""

def test_get_similar_items_empty_dict():
    assert get_similar_item("foobar", {}) == ""

def test_get_similar_items_of_same_ratio():
    thisdict = {"bworde": "0.8", "sworde": "0.8"}
    assert get_similar_item("word", thisdict) == "bworde"