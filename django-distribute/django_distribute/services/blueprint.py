"""
Service for managing blueprint strings and their JSON representations.

Functions:
    generate_bp_from_json: Generates blueprint string from JSON.
    generate_book: Generates blueprint book JSON representation.
    generate_chest: Generates requester chest JSON representation.
    generate_item: Generates item JSON representation.
    convert_blueprint: Converts blueprints to JSON representation.
"""

import base64
import json
import zlib

from django_distribute.data.item import Item
from django_distribute.services.helper import transform_string


def generate_bp_from_json(json_obj: object) -> str:
    """
    Generates a blueprint string from a JSON object representation.

    The JSON is compressed then encoded using
    base64 with a version byte at the front.

    :param object json_obj: JSON representation of the blueprint.
    :return: The blueprint string.
    :rtype: str
    """
    json_str = json.dumps(json_obj).replace(" ", "").replace("@", " ")
    json_bytes = json_str.encode("utf-8")
    json_compressed = zlib.compress(json_bytes, 9)
    return (b"0" + base64.b64encode(json_compressed)).decode("utf-8")


def generate_book(chests: list) -> object:
    """
    Generates a JSON representation of a blueprint book.

    :param list chests: List of JSON-represented requester chests.
    :returns: JSON-represented blueprint book.
    :rtype: object
    """
    description = (
        "Blueprints@generated@by@Rocket@Request.@Each@chest@corresponds@to@a@silo."
    )
    return {
        "blueprint_book": {
            "blueprints": chests,
            "description": description,
            "icons": [
                {"index": 1, "signal": {"name": "rocket-silo"}},
                {"index": 2, "signal": {"name": "requester-chest"}},
            ],
            "item": "blueprint-book",
            "label": "Silo@Item@Requests",
            "active_index": 0,
            "version": 562949958205441,
        }
    }


def generate_chest(silo_num: int, items: list) -> object:
    """
    Generates a JSON representation of a requester chest.

    :param int silo_num: The silo that the chest is assigned to.
    :param list items: List of JSON-represented items.
    :return: JSON-represented requester chest.
    :rtype: object
    """
    return {
        "blueprint": {
            "icons": [{"signal": {"name": "requester-chest"}, "index": 1}],
            "entities": [
                {
                    "entity_number": 1,
                    "name": "requester-chest",
                    "position": {"x": 0.0, "y": 0.0},
                    "request_filters": {
                        "sections": [{"index": 1, "filters": items}],
                        "trash_not_requested": True,
                    },
                }
            ],
            "item": "blueprint",
            "label": str(silo_num),
            "version": 562949958205441,
        },
        "index": silo_num - 1,
    }


def generate_item(index: int, name: str, count: int) -> object:
    """
    Generates a JSON representation of an item.

    :param int index: 1-based request slot.
    :param str name: The item name in slug format.
    :param int count: The item count.
    :return: JSON-represented item.
    :rtype: object
    """
    return {
        "index": index,
        "name": name,
        "quality": "normal",
        "comparator": "=",
        "count": count,
    }


def convert_blueprint(blueprint: str) -> object:
    """
    Converts a blueprint string to its JSON object representation.

    :param str blueprint: The blueprint string to convert.
    :return: JSON-represented blueprint.
    :rtype: object
    """
    decoded_bp = base64.b64decode(blueprint[1:])
    decomp_bp = zlib.decompress(decoded_bp)
    json_str = decomp_bp.decode("utf-8")
    return json.loads(json_str)


def extract_items_from_json(json_rep: object, item_data: dict[str, Item]) -> list[Item]:
    """
    Extracts all Item entities from a JSON blueprint representation.

    :param object json_rep: The JSON representation of a blueprint.
    :return: Items extracted from the JSON.
    :rtype: list[Item]
    """
    itemlist = []
    for entity in json_rep["blueprint"]["entities"]:
        if entity["name"] == "space-platform-hub":
            pass
        elif entity["name"] == "long-handed-inserter":
            itemlist.append(item_data["Long-handed inserter"])
        else:
            key = entity["name"].replace("-", " ").capitalize()
            item = item_data.get(key)
            if item:
                itemlist.append(item)
            # TODO: Deal with invalid item
            else:
                print(key)
    return itemlist
