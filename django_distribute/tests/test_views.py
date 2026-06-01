"""Display, request, and session tests on views."""

import cProfile
from pathlib import Path
import pstats
import tomllib
from unittest.mock import patch

from django.test import tag
from django.urls import reverse
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from django_distribute.data.constants import Errors
from django_distribute.data.items import ITEMS
from django_distribute.exceptions import (
    ChestIndexException,
    InvalidBlueprintException,
    InvalidItemException,
)


@tag("views")
class IndexViewTests(TestCase):
    def test_itemlist_no_items(self):
        """
        If no items have been added, an appropriate
        message is displayed in the item list.
        """
        response = self.client.get(reverse("distribute:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Errors.NO_ITEMS_ADDED)
        self.assertContains(
            response,
            '<th id="item-th" scope="col">' + Errors.NO_ITEMS_ADDED + "</th>",
            html=True,
        )
        self.assertNotContains(
            response, '<th id="item-th" scope="col">Item</th>', html=True
        )
        self.assertNotContains(
            response, '<th id="count-th" scope="col">Count</th>', html=True
        )

    @given(st.integers(), st.integers())
    def test_elements_displayed_with_items(self, n1, n2):
        """
        When the session contains items, the item names, counts,
        table headers, and remove buttons are displayed.
        """
        session = self.client.session
        session["itemlist"] = {"Foo": n1, "Bar": n2}
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
        self.assertContains(response, f"{n1}")
        self.assertContains(response, "Bar")
        self.assertContains(response, f"{n2}")
        self.assertContains(response, 'data-item-name="Foo">')
        self.assertContains(response, 'data-item-name="Bar">')

    def test_distribute_error_displayed(self):
        """If the error for distribute is set, it is displayed."""
        session = self.client.session
        session["distribute_error"] = Errors.ADD_ITEMS_DISTRIBUTE
        session.save()
        response = self.client.get(reverse("distribute:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Errors.ADD_ITEMS_DISTRIBUTE)
        self.assertContains(
            response,
            '<div id="distribute-error" class="error">'
            + Errors.ADD_ITEMS_DISTRIBUTE
            + "</div>",
            html=True,
        )
        self.assertNotIn("distribute_error", self.client.session)

    def test_suggestions_list(self):
        """Ensure the full suggestion list is passed correctly."""
        response = self.client.get(reverse("distribute:index"))
        for item_name in ITEMS:
            self.assertContains(
                response, f'<option value="{item_name}">{item_name}</option>'
            )

    def test_footer_version(self):
        """Version in the footer is set correctly."""
        conf = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(conf, "rb") as f:
            version = tomllib.load(f)["project"]["version"]
        response = self.client.get(reverse("distribute:index"))
        self.assertContains(response, version)

    def test_build_date(self):
        """Build date is set by the build date context processor."""
        expected = (Path(__file__).parent.parent / "BUILD_DATE").read_text()
        response = self.client.get(reverse("distribute:index"))
        self.assertContains(response, expected)


@tag("views")
class ItemCollectionViewTests(TestCase):
    @given(st.integers(min_value=1, max_value=100000))
    def test_valid_item_collection(self, n):
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": n},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"]["Transport belt"], n)

    @given(
        st.integers(min_value=1, max_value=50000),
        st.integers(min_value=1, max_value=50000),
    )
    def test_item_collection_on_existing_item(self, n1, n2):
        """Item count is incremented on an additional add."""
        self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": n1},
        )
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": n2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"]["Transport belt"], n1 + n2)

    @given(st.integers(min_value=1))
    def test_response_on_invalid_item(self, n):
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Foobar", "user-count": n},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"], "Invalid item")

    @given(st.integers(max_value=-1))
    def test_response_on_invalid_count(self, n):
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": 0},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"], "Invalid count")

        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": n},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"], "Invalid count")

    def test_response_on_count_value_error(self):
        response = self.client.post(
            reverse("distribute:collection"),
            {"user-item": "Transport belt", "user-count": "Foobar"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["itemlist"], "Invalid count")

    def test_item_collection_rejects_get(self):
        response = self.client.get(reverse("distribute:collection"))
        self.assertEqual(response.status_code, 400)


@tag("views")
class RemoveViewTests(TestCase):
    @given(st.integers(min_value=1), st.integers(min_value=1))
    def test_remove_item(self, n1, n2):
        """
        The posted item is removed from the itemlist
        and is not in the returned JSON.
        """
        session = self.client.session
        session["itemlist"] = {"Foo": n1, "Bar": n2}
        session.save()
        response = self.client.post(reverse("distribute:remove"), {"user-item": "Foo"})
        self.assertNotIn("Foo", self.client.session)
        self.assertEqual(response.json()["itemlist"]["Bar"], n2)

    def test_remove_nonexistent_item(self):
        """
        Itemlist should be unchanged on removal of nonexistent item.
        """
        session = self.client.session
        session["itemlist"] = {"Foo": 12, "Bar": 7}
        session.save()
        response = self.client.post(reverse("distribute:remove"), {"user-item": "Asdf"})
        itemlist = response.json()["itemlist"]
        self.assertEqual(itemlist["Foo"], 12)
        self.assertEqual(itemlist["Bar"], 7)
        self.assertEqual(2, len(itemlist))

    def test_remove_rejects_get(self):
        response = self.client.get(reverse("distribute:remove"))
        self.assertEqual(response.status_code, 400)


@tag("views")
class DistributableViewTests(TestCase):
    def test_redirect_on_no_items(self):
        """
        Test redirect back to index with an error on an empty itemlist.
        """
        response = self.client.get(reverse("distribute:distributable"), follow=True)
        self.assertRedirects(response, reverse("distribute:index"))
        self.assertContains(response, Errors.ADD_ITEMS_DISTRIBUTE)

    def test_distributable_missing_num_silos(self):
        """Return bad request on post if num_silos is missing."""
        session = self.client.session
        session["itemlist"] = {"Foo": 12, "Bar": 7}
        session.save()
        response = self.client.post(reverse("distribute:distributable"))
        self.assertEqual(response.status_code, 400)

    @given(
        st.integers(min_value=1, max_value=1000),
        st.integers(min_value=1, max_value=1000),
        st.integers(min_value=1, max_value=100),
    )
    def test_distributable_flow(self, n1, n2, n3):
        """
        POST valid num_silos with itemlist present, assert
        redirect to results and session stores num_silos.
        """
        session = self.client.session
        session["itemlist"] = {"Transport belt": n1, "Pipe": n2}
        session.save()
        response = self.client.post(
            reverse("distribute:distributable"), {"num-silos": n3}, follow=True
        )
        self.assertRedirects(response, reverse("distribute:results"))
        self.assertEqual(self.client.session["num_silos"], f"{n3}")


@tag("views")
class ResultsViewTests(TestCase):
    def test_redirect_on_missing_num_silos(self):
        session = self.client.session
        session["itemlist"] = {"Transport belt": 100}
        session.save()
        response = self.client.get(reverse("distribute:results"), follow=True)
        self.assertRedirects(response, reverse("distribute:index"))

    def test_redirect_on_missing_itemlist(self):
        session = self.client.session
        session["num_silos"] = 1
        session.save()
        response = self.client.get(reverse("distribute:results"), follow=True)
        self.assertRedirects(response, reverse("distribute:index"))

    def test_results_renders_distribution_summary_when_valid_session(self):
        """
        With valid itemlist and num_silos, assert the results page
        contains num_launches, num_cycles, and distribution output.
        """
        session = self.client.session
        session["itemlist"] = {"Transport belt": 80, "Chemical plant": 6, "Thruster": 4}
        session["num_silos"] = 2
        session.save()
        response = self.client.get(reverse("distribute:results"))
        self.assertContains(response, "<td>Available silos</td><td>2</td>", html=True)
        self.assertContains(response, "<td>Required launches</td><td>3</td>", html=True)
        self.assertContains(
            response, "<td>Required launch cycles</td><td>2</td>", html=True
        )
        self.assertContains(response, '<td scope="row">Chemical plant</td>', html=True)
        self.assertContains(response, "<h3>Cycle 2 of 2</h3>", html=True)
        self.assertContains(response, "<h3>Silo 2 (1000 kg)</h3>", html=True)
        conf = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(conf, "rb") as f:
            version = tomllib.load(f)["project"]["version"]
        self.assertContains(response, version)

    def test_redirect_on_invalid_num_silos(self):
        """Redirects back to index if the number of silos is not an integer."""
        session = self.client.session
        session["num_silos"] = "Foobar"
        session.save()
        response = self.client.get(reverse("distribute:results"), follow=True)
        self.assertRedirects(response, reverse("distribute:index"))

    @given(st.integers(max_value=0))
    def test_redirect_on_non_positive_num_silos(self, n1):
        """Redirects back to index if the number of silos is not positive."""
        session = self.client.session
        session["num_silos"] = n1
        session.save()
        response = self.client.get(reverse("distribute:results"), follow=True)
        self.assertRedirects(response, reverse("distribute:index"))

    def test_redirect_on_too_many_silos(self):
        """Redirects back to index if the number of silos is over the limit."""
        session = self.client.session
        session["num_silos"] = "101"
        session.save()
        response = self.client.get(reverse("distribute:results"), follow=True)
        self.assertRedirects(response, reverse("distribute:index"))

    @patch(
        "django_distribute.views.build_consolidated_blueprint",
        side_effect=ChestIndexException(),
    )
    @patch("django_distribute.views.zip")
    @patch("django_distribute.views.build_consolidated_load")
    @patch("django_distribute.views.build_consolidated_invs")
    @patch("django_distribute.views.build_distribution")
    @patch("django_distribute.views.distribute_items")
    def test_results_exceed_chest_slots(
        self, mock_di, mock_bd, mock_bci, mock_bcl, mock_zip, mock_bcb
    ):
        """An error is passed to blueprint as items exceed available slots."""
        session = self.client.session
        session["num_silos"] = 1
        session["itemlist"] = {"Transport belt": 1}
        session.save()
        response = self.client.get(reverse("distribute:results"))
        self.assertContains(response, Errors.ITEMS_EXCEED_SLOTS)


@tag("views")
class ContactViewTests(TestCase):
    def test_contact_page(self):
        """Test that elements can be found on the contact page."""
        response = self.client.get(reverse("distribute:contact"))
        self.assertContains(response, "Contact me")
        self.assertContains(response, "Issues")
        self.assertContains(response, "Feedback")
        self.assertContains(response, "Email")
        self.assertContains(response, "Find a bug or incorrect data?")

    def test_footer_version(self):
        """Version in the footer is set correctly."""
        conf = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(conf, "rb") as f:
            version = tomllib.load(f)["project"]["version"]
        response = self.client.get(reverse("distribute:contact"))
        self.assertContains(response, version)


@tag("views")
class AboutViewTests(TestCase):
    def test_about_page(self):
        """Test that elements can be found on the about page."""
        response = self.client.get(reverse("distribute:about"))
        self.assertContains(response, "About")
        self.assertContains(response, "Why?")
        self.assertContains(response, "Source")
        self.assertContains(
            response,
            "If you would like to check out or contribute to the source code, it is available on GitHub",
        )

    def test_footer_version(self):
        """Version in the footer is set correctly."""
        conf = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(conf, "rb") as f:
            version = tomllib.load(f)["project"]["version"]
        response = self.client.get(reverse("distribute:about"))
        self.assertContains(response, version)


@tag("views")
class ResetViewTests(TestCase):
    def test_itemlist_reset(self):
        """Itemlist is cleared on reset."""
        session = self.client.session
        session["itemlist"] = {"Transport belt": 80, "Chemical plant": 6, "Thruster": 4}
        session.save()
        self.client.get(reverse("distribute:reset"))
        self.assertEqual(self.client.session["itemlist"], {})

    def test_itemlist_reset_empty(self):
        """Empty itemlist is cleared on reset."""
        session = self.client.session
        session["itemlist"] = {}
        session.save()
        self.client.get(reverse("distribute:reset"))
        self.assertEqual(self.client.session["itemlist"], {})

    def test_no_itemlist_reset(self):
        """If there is no itemlist, an empty one is set."""
        self.client.get(reverse("distribute:reset"))
        self.assertEqual(self.client.session["itemlist"], {})


class ViewProfileTests(TestCase):
    @tag("slow", "profile")
    def test_profile_distribution(self):
        """Collects cProfile statistics."""
        n1 = 100000
        n2 = 100000
        n3 = 2

        with cProfile.Profile() as profile:
            self.client.post(
                reverse("distribute:collection"),
                {"user-item": "Transport belt", "user-count": n1},
            )
            self.client.post(
                reverse("distribute:collection"),
                {"user-item": "Chemical plant", "user-count": n2},
            )

            self.client.post(
                reverse("distribute:distributable"), {"num-silos": n3}, follow=True
            )
        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.print_stats()
        results.dump_stats("results.prof")


@tag("views")
class ImportBlueprintViewTests(TestCase):
    valid_bp = "0eNqrVkrKKU0tKMrMK1GyqlZKzSvJLMlMLVayiq5WykvMTVWyUiopSswrLsgvKtFNSs0pUaqNra0FACAuE/s="

    def test_import_blueprint_get(self):
        """Sending import a get request will return a bad response."""
        response = self.client.get(reverse("distribute:import"))
        self.assertEqual(response.status_code, 400)

    def test_import_blueprint(self):
        """Importing a blueprint sets the itemlist."""
        response = self.client.post(
            reverse("distribute:import"),
            {"blueprint-input": self.valid_bp},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["itemlist"], {"Transport belt": 1})

    @patch(
        "django_distribute.views.extract_items_from_json",
        side_effect=InvalidItemException("Foobar"),
    )
    def test_import_invalid_item(self, mock):
        """Invalid item sets the item import error."""
        response = self.client.post(
            reverse("distribute:import"),
            {"blueprint-input": self.valid_bp},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.session["import_error"], f"{Errors.INVALID_ITEM}Foobar"
        )

    @patch(
        "django_distribute.views.convert_blueprint",
        side_effect=InvalidBlueprintException("Foobar"),
    )
    def test_import_invalid_blueprint(self, mock):
        """Invalid import sets the import error."""
        response = self.client.post(
            reverse("distribute:import"),
            {"blueprint-input": self.valid_bp},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["import_error"], Errors.IMPORT_ERROR)

    def test_import_empty(self):
        """Empty blueprint import does not affect the existing itemlist."""
        session = self.client.session
        item = {"Transport belt": 1}
        session["itemlist"] = item
        session.save()
        response = self.client.post(
            reverse("distribute:import"),
            {"blueprint-input": ""},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["itemlist"], item)

    def test_import_long_blueprint(self):
        """Importing a blueprint that is too long does not import items."""
        longstring = "a" * 1000000
        session = self.client.session
        item = {"Transport belt": 1}
        session["itemlist"] = item
        session.save()
        response = self.client.post(
            reverse("distribute:import"), {"blueprint-input": longstring}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("distribute:index"))
        self.assertEqual(self.client.session["itemlist"], item)

    @patch("django_distribute.views.is_max_count", return_value=True)
    def test_import_too_many_items(self, mock):
        """Importing a blueprint with too many items sets an import error."""
        session = self.client.session
        item = {"Transport belt": 1}
        session["itemlist"] = item
        session.save()
        response = self.client.post(
            reverse("distribute:import"),
            {"blueprint-input": self.valid_bp},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.session["import_error"], Errors.BP_ITEMS_EXCEED_MAX
        )
        self.assertEqual(self.client.session["itemlist"], {"Transport belt": 1})
