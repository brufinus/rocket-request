import base64
from unittest import TestCase
import zlib

from django.test import tag

from django_distribute.data.items import ITEMS
from django_distribute.services.blueprint import \
    InvalidBlueprintException, convert_blueprint, extract_items_from_json, generate_book, generate_bp_from_json, generate_chest, generate_item
from django_distribute.exceptions import InvalidItemException

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
    
    def test_convert_blueprint(self):
        """Converts the blueprint string to a JSON object."""
        bp_string = "0eNrFV9uO2yAQ/Ree7ZUvOJeV2pe+9g+qyCIOTlExuIB3u1353zsDrOPdpFVbVPXJzHjmcGbOgJNncpQTH41Qjtw/kxO3nRGjE1qRe/KBjewoue6dYQ/cWKHOQiluRskUd5ZkRHRaWXL/6ZlYcVZMIoZ7Gjkk25F1PJe6Yx4tI4oN6FdsehCWzJCsTvwbuS/nQ0a4csIJHrC88dSqaThyAwFL7nlSuZuM4Q7wRm1FIPpMACavMvIEj7qZ5+wKo1kwhLLcOPBdI9R3TcSo7hogeBKGdyGA3sDcLJjQH2VHbVx+5PImtz9Drurtgm21ZCYfoePyBnATgcu7m2VX9e4C5AUB7VyvzZB/no7XeIUHK4Ch4V8nbl3bCwnNsvjeBspBo0W8bFmDAEv0KmIhwCUAGD2wM0yP6HLbCa6QEuu+AJWvE5PAHUcE+DGsttPDyAxzGkoh77xjwkEti6LAqWFA6AGgeyYtXzGp3746rAoCBu1x6nvP05mJr6odhMUpb3Gs4ZWvtx0Y1CQA5yX8qs31/jJfoxh57nR+NsD1dN3il1Godm8nYYc0bfeZnyYZTwIcHz1orARtUHMVgXiQq80pnkDH4rntJ3nWhsHej0w4LOYkLsrF88mkbGPZtrWQanvBT0vTefsSB0VgydHshOkm4W7HoTPuhex6YaCnl5shdgjcnMEEwiCw70JxvAt8wxlqS9/I/p7M8wEJXOqLV8i/KE84PrRhyhIq/OWkv6q2uBry+f83+zDjJD5CJrb0U7nJqgxupOqQxXXp1/jIaPBT9G+Cf1PBehv8WwrrXR3W28u6pPDMSgz1qAVaGOwtfIdXl7f2CFfuQ15V0qz070q0aty2ogHFZ2TVbrO26CurCQwrWvp3TbB2xTpv5zH325VVF2F3/wSLrq1qGy0sta4DF+/Nahoj0QvWPljUR8ZqvRcsRIGuO/Fy9q++TvELspl/dqX3eOOEQ4JD9LMP5F8DlIkARWJ+6v7JDaiXnxiJEjSpEjSJEjSJEjSJEjSpEtBUCWiqBDRRApooAU2U4K8bsIkAdVIBdflb6XAl4jcZgi5/VDIiGfzQBt9Hrc5HLcDj/5/gFs2m2tP9vtlVRUNpOc8/ABTZNCw="
        expected = {"blueprint":{"description":"Capableoftraversinginnerplanets","icons":[{"signal":{"type":"space-location","name":"nauvis"},"index":1}],"entities":[{"entity_number":1,"name":"gun-turret","position":{"x":-2,"y":-35}},{"entity_number":5,"name":"inserter","position":{"x":-3.5,"y":-32.5},"direction":4},{"entity_number":6,"name":"transport-belt","position":{"x":-2.5,"y":-32.5},"direction":4},{"entity_number":237,"name":"solar-panel","position":{"x":-5.5,"y":1.5}},{"entity_number":238,"name":"space-platform-hub","position":{"x":0,"y":0},"request_filters":{"sections":[{"index":1},{"index":2,"filters":[{"index":1,"name":"electromagnetic-science-pack","quality":"normal","comparator":"=","count":1000}],"active":False},{"index":3,"active":False}],"request_from_buffers":True},"request_missing_construction_materials":True},{"entity_number":395,"name":"pipe-to-ground","position":{"x":2.5,"y":28.5},"direction":8}],"schedules":[{"locomotives":[238],"schedule":{"records":[{"station":"fulgora","wait_conditions":[{"type":"all_requests_satisfied","compare_type":"and"},{"type":"circuit","compare_type":"and","condition":{"first_signal":{"name":"firearm-magazine"},"constant":4,"comparator":">"}}]},{"station":"nauvis","wait_conditions":[{"type":"all_requests_satisfied","compare_type":"and"},{"type":"item_count","compare_type":"and","condition":{"first_signal":{"name":"electromagnetic-science-pack"},"constant":0,"comparator":"="}},{"type":"circuit","compare_type":"and","condition":{"first_signal":{"name":"firearm-magazine"},"constant":4,"comparator":">"}}]}]}}],"wires":[[16,2,37,2],[16,2,31,2],[31,2,47,2],[46,2,61,2],[62,2,77,2],[74,2,83,2],[77,2,83,2],[143,2,162,2],[160,2,174,2],[163,2,238,2],[192,2,193,2],[214,1,238,1],[236,2,242,2],[238,2,286,2],[238,2,246,2],[238,2,251,2],[241,2,245,2],[280,2,286,2],[286,2,297,2],[286,2,303,2],[303,2,304,2],[303,2,327,2],[304,2,332,2],[327,2,344,2],[332,2,349,2],[344,2,374,2],[349,2,377,2]],"tiles":[{"position":{"x":-3,"y":-36},"name":"space-platform-foundation"},{"position":{"x":-2,"y":-36},"name":"space-platform-foundation"},{"position":{"x":-1,"y":-36},"name":"space-platform-foundation"},{"position":{"x":0,"y":-36},"name":"space-platform-foundation"},{"position":{"x":1,"y":-36},"name":"space-platform-foundation"},{"position":{"x":2,"y":-36},"name":"space-platform-foundation"},{"position":{"x":-3,"y":-35},"name":"space-platform-foundation"},{"position":{"x":-2,"y":-35},"name":"space-platform-foundation"},{"position":{"x":-1,"y":-35},"name":"space-platform-foundation"},{"position":{"x":0,"y":-35},"name":"space-platform-foundation"},{"position":{"x":1,"y":-35},"name":"space-platform-foundation"},{"position":{"x":2,"y":-35},"name":"space-platform-foundation"},{"position":{"x":-3,"y":-34},"name":"space-platform-foundation"},{"position":{"x":-2,"y":-34},"name":"space-platform-foundation"},{"position":{"x":-1,"y":-34},"name":"space-platform-foundation"},{"position":{"x":0,"y":-34},"name":"space-platform-foundation"},{"position":{"x":1,"y":-34},"name":"space-platform-foundation"},{"position":{"x":2,"y":-34},"name":"space-platform-foundation"},{"position":{"x":-6,"y":-33},"name":"space-platform-foundation"},{"position":{"x":1,"y":31},"name":"space-platform-foundation"}],"item":"blueprint","label":"Longboi","version":562949958205441}}
        res = convert_blueprint(bp_string)
        self.assertEqual(res, expected)
    
    def test_convert_invalid_blueprints(self):
        """Invalid blueprints raise InvalidBlueprintExceptions."""
        bp_string = "This is an invalid blueprint string"
        with self.assertRaises(InvalidBlueprintException):
            convert_blueprint(bp_string)
        bp_string = "@@@@"
        with self.assertRaises(InvalidBlueprintException):
            convert_blueprint(bp_string)

        bp_string = "multipleoffouryes"
        with self.assertRaises(InvalidBlueprintException):
            convert_blueprint(bp_string)

        # Non-dict object
        bp_string = "0eNpTSsvPT0osUgIADFgCvg=="
        with self.assertRaises(InvalidBlueprintException):
            convert_blueprint(bp_string)
        
        # dict object but not a blueprint.
        bp_string = "0eNqrVkrLz1eyUkpKLFKqBQAdegQ0"
        with self.assertRaises(InvalidBlueprintException):
            convert_blueprint(bp_string)

    def test_extract_items_from_json(self):
        """Items are extracted from JSON representation."""
        expected = [ITEMS["Long-handed inserter"], ITEMS["Transport belt"]]
        json_rep = {
            "blueprint": {
                "entities": [
                    {"name": "space-platform-hub"},
                    {"name": "long-handed-inserter"},
                    {"name": "transport-belt"}
                ]
            }
        }
        res = extract_items_from_json(json_rep, ITEMS)
        self.assertEqual(res, expected)
    
    def test_extract_invalid_item_from_json(self):
        """Importing an invalid item throws an InvalidItemException."""
        json_rep = {
            "blueprint": {
                "entities": [
                    {"name": "foobar"}
                ]
            }
        }
        with self.assertRaises(InvalidItemException) as e:
            extract_items_from_json(json_rep, ITEMS)
        
        self.assertEqual(str(e.exception), "Invalid item imported: Foobar")
