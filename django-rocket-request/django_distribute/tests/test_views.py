"""Display, request, and session tests on views."""

from django.http import HttpResponseBadRequest
from django.test import TestCase
from django.urls import reverse
from django_distribute.data.constants import Errors
from django_distribute.data.items import ITEMS


class IndexViewTests(TestCase):
    def test_itemlist_no_items(self):
        """
        If no items have been added, an appropriate
        message is displayed in the item list.
        """
        response = self.client.get(reverse("distribute:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Errors.NO_ITEMS_ADDED)
        self.assertNotContains(
            response, '<th id="item-th" scope="col">Item</th>', html=True
        )
        self.assertNotContains(
            response, '<th id="count-th" scope="col">Count</th>', html=True
        )

    def test_elements_displayed_with_items(self):
        """
        When the session contains items, the item names, counts,
        table headers, and remove buttons are displayed.
        """
        session = self.client.session
        session["itemlist"] = {"Foo": 12, "Bar": 7}
        session.save()
        response = self.client.get(reverse("distribute:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<th id="item-th" scope="col">Item</th>', html=True
        )
        self.assertContains(
            response, '<th id="count-th" scope="col">Count</th>', html=True
        )
        self.assertContains(response, "Foo")
        self.assertContains(response, "12")
        self.assertContains(response, "Bar")
        self.assertContains(response, "7")
        self.assertContains(
            response,
            '<button id="remove-button" data-item-name="Foo">Remove</button>',
            html=True,
        )
        self.assertContains(
            response,
            '<button id="remove-button" data-item-name="Bar">Remove</button>',
            html=True,
        )

    def test_distribute_error_displayed(self):
        """If the error for distribute is set, it is displayed."""
        session = self.client.session
        session["distribute_error"] = Errors.ADD_ITEMS_DISTRIBUTE
        session.save()
        response = self.client.get(reverse("distribute:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Errors.ADD_ITEMS_DISTRIBUTE)
        self.assertNotIn("distribute_error", self.client.session)

    def test_suggestions_list(self):
        """Ensure the full suggestion list is passed correctly."""
        response = self.client.get(reverse("distribute:index"))
        for item_name in ITEMS:
            self.assertContains(
                response, f'<option value="{item_name}">{item_name}</option>'
            )


class ItemCollectionViewTests(TestCase):
    def test_valid_item_collection(self):
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": 20},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"]["Transport belt"], 20)

    def test_item_collection_on_existing_item(self):
        """Item count is incremented on an additional add."""
        self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": 20},
        )
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": 7},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"]["Transport belt"], 27)

    def test_response_on_invalid_item(self):
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Foobar", "user-count": 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"], "Invalid item")

    def test_response_on_invalid_count(self):
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": 0},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"], "Invalid count")

        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": -1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"], "Invalid count")

    def test_item_collection_rejects_get(self):
        response = self.client.get(reverse("distribute:collection"))
        self.assertEqual(response.status_code, 400)


class RemoveViewTests(TestCase):
    def test_remove_item(self):
        response = self.client.post(reverse("distribute:remove"))


class ResultsViewTests(TestCase):
    def test_results(self):
        self.assertEqual(1, 1)
