import base64
from unittest import TestCase
import zlib

from django.test import tag

from django_distribute.services.blueprint import \
    generate_book, generate_bp_from_json, generate_chest, generate_item

@tag("bp")
class TestBlueprint(TestCase):
    def test_generate_bp_from_json(self):
        """Generates blueprint string from JSON."""
        bp_string = "0eNq9VMtOwzAQ/Jc9O1UdEtRE4sgHwBUhy0kNsYjt1I+oVZV/Z500bZEKokLlFO96d2Z3PMoeqjaIzkrtWWXMB5T7U8ZB+XIWxjtZGz2lnXzXvI05zZWAEqzYBOG8sEnd4BcGAlKvxRZKOpDzer/rYn0vrQ+YITPAVJHQs850eCUgtJdeiol2DHZMB1UJi9DkO3oCnXHYZ3TkRKykyBc5gR2eaLFa5Mhy6GFvssVGFwudqGPPRDbPT+BY8SV7oPaWa9cZ65NKtJF5g3vhlHiljVXjjrVRHbfcGxwaHsZEiJLS5TKqM+97xMQllKxRjq7l+kpMVC3qhmO5hmnj2azNGkpvgxjirfRCYdvpdQm0HOfH3PPjE8Wwx4VH+fL7tMiKIl+lyzzL6Ol5xtH/2x/pzfyR3cgftQ2uwWmuNAYBxbfsGF60iW8Q21+Lffd3g6S/Mgi9BJSMPxoCHJXsBZu99APe8AkpWIwB"
        json = {"blueprint_book":{"blueprints":[{"blueprint":{"icons":[{"signal":{"name":"requester-chest"},"index":1},{"signal":{"type":"virtual","name":"signal-1"},"index":2}],"entities":[{"entity_number":1,"name":"requester-chest","position":{"x":-95.5,"y":-198.5},"request_filters":{"sections":[{"index":1,"filters":[{"index":1,"name":"transport-belt","quality":"normal","comparator":"=","count":100},{"index":2,"name":"chemical-plant","quality":"normal","comparator":"=","count":2}]}],"trash_not_requested":True}}],"item":"blueprint","label":"REQ1","version":562949958205441},"index":0},{"blueprint":{"icons":[{"signal":{"name":"requester-chest"},"index":1},{"signal":{"type":"virtual","name":"signal-2"},"index":2}],"entities":[{"entity_number":1,"name":"requester-chest","position":{"x":-94.5,"y":-198.5},"request_filters":{"sections":[{"index":1,"filters":[{"index":1,"name":"crusher","quality":"normal","comparator":"=","count":10,"max_count":10},{"index":2,"name":"thruster","quality":"normal","comparator":"=","count":3}]}],"trash_not_requested":True}}],"item":"blueprint","label":"REQ2","version":562949958205441},"index":1}],"item":"blueprint-book","active_index":0,"version":562949958205441}}
        res = generate_bp_from_json(json)
        self.assertEqual(res, bp_string)

    def test_generate_bare_blueprint_book_json(self):
        """Generates blueprint book with no chests."""
        expected = {
            "blueprint_book": {
                "active_index": 0,
                "blueprints": [{}],
                "description": "Blueprints@generated@by@Rocket@Request.@Each@chest@corresponds@to@a@silo.",
                "icons": [
                    {"index": 1, "signal": {"name": "rocket-silo"}},
                    {"index": 2, "signal": {"name": "requester-chest"}},
                ],
                "item": "blueprint-book",
                "label": "Silo@Item@Requests",
                "version": 562949958205441,
            }
        }
        res = generate_book([{}]) 
        self.assertEqual(res, expected)

    def test_generate_bare_chest_json(self):
        """Generates chest JSON with no items."""
        expected = {
            "blueprint": {
                "icons": [{"signal": {"name": "requester-chest"}, "index": 1}],
                "entities": [
                    {
                        "entity_number": 1,
                        "name": "requester-chest",
                        "position": {"x": 0.0, "y": 0.0},
                        "request_filters": {
                            "sections": [{"index": 1, "filters": [{}]}],
                            "trash_not_requested": True,
                        },
                    }
                ],
                "item": "blueprint",
                "label": "1",
                "version": 562949958205441,
            },
            "index": 0,
        }
        res = generate_chest(1, [{}])
        self.assertEqual(res, expected)

    def test_generate_item_json(self):
        item = {"index":1,"name":"transport-belt","quality":"normal","comparator":"=","count":100}
        self.assertEqual(generate_item(1, "transport-belt", 100), item)

    def test_generate_populated_bp(self):
        text = b'{"blueprint_book":{"blueprints":[{"blueprint":{"icons":[{"signal":{"name":"requester-chest"},"index":1}],"entities":[{"entity_number":1,"name":"requester-chest","position":{"x":0.0,"y":0.0},"request_filters":{"sections":[{"index":1,"filters":[{"index":1,"name":"transport-belt","quality":"normal","comparator":"=","count":100},{"index":2,"name":"chemical-plant","quality":"normal","comparator":"=","count":2}]}],"trash_not_requested":true}}],"item":"blueprint","label":"1","version":562949958205441},"index":0},{"blueprint":{"icons":[{"signal":{"name":"requester-chest"},"index":1}],"entities":[{"entity_number":1,"name":"requester-chest","position":{"x":0.0,"y":0.0},"request_filters":{"sections":[{"index":1,"filters":[{"index":1,"name":"crusher","quality":"normal","comparator":"=","count":10},{"index":2,"name":"thruster","quality":"normal","comparator":"=","count":3}]}],"trash_not_requested":true}}],"item":"blueprint","label":"2","version":562949958205441},"index":1}],"description":"Blueprints generated by Rocket Request. Each chest corresponds to a silo.","icons":[{"index":1,"signal":{"name":"rocket-silo"}},{"index":2,"signal":{"name":"requester-chest"}}],"item":"blueprint-book","label":"Silo Item Requests","active_index":0,"version":562949958205441}}'
        compressed = zlib.compress(text, 9)
        encoded = base64.b64encode(compressed)
        v_encoded = b'0' + encoded
        expected = v_encoded.decode("utf-8")

        itemset1 = [generate_item(1, "transport-belt", 100), generate_item(2, "chemical-plant", 2)]
        itemset2 = [generate_item(1, "crusher", 10), generate_item(2, "thruster", 3)]
        chests = [generate_chest(1, itemset1), generate_chest(2, itemset2)]
        book = generate_book(chests)
        res = generate_bp_from_json(book)
        self.assertEqual(res, expected)
