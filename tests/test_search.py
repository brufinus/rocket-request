from data.items import ITEMS
from services.search import search_item, search_similar_item


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

def test_search_item_by_key():
    assert len(search_item("item1", dictionary)) > 0

def test_search_item_by_keyword():
    assert len(search_item("alias", dictionary)) > 0
    assert len(search_item("foo", dictionary)) > 0
    assert len(search_item("bar", dictionary)) > 0

def test_validate_correct_item_by_keyword():
    assert search_item("belt", ITEMS) == "transportbelt"

def test_invalid_item():
    assert len(search_item("pootis", dictionary)) == 0

def test_search_similar_item():
    assert search_similar_item("item", dictionary) == "item1"
    thisdict = {"grapple": "0.73", "orange": "0.4", "apple": "0.89"}
    assert search_similar_item("aple", thisdict) == "apple"

def test_get_with_confidence():
    # Returns sword as it's above the confidence threshold.
    thisdict = {"sword": "0.89", "word": "1.0"}
    assert search_similar_item("word", thisdict) == "sword"

def test_no_similar_items():
    assert search_similar_item("banana", dictionary) == ""

def test_search_similar_items_no_item():
    assert search_similar_item("", dictionary) == ""

def test_search_similar_items_empty_dict():
    assert search_similar_item("foobar", {}) == ""

def test_search_similar_items_of_same_ratio():
    thisdict = {"bworde": "0.8", "sworde": "0.8"}
    assert search_similar_item("word", thisdict) == "bworde"
