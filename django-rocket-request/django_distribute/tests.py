from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class IndexViewTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse("distribute:index"))
        self.assertEqual(response.status_code, 200)


class ResultsViewTests(TestCase):
    def test_results(self):
        self.assertEqual(1, 1)
