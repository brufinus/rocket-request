from unittest import TestCase

from django_distribute.services.helper import get_formatted_float, transform_string


class TestHelper(TestCase):
    def test_formatted_whole_number(self):
        self.assertEqual(get_formatted_float(1.0), "1")
    
    def test_formatted_non_whole_number(self):
        self.assertEqual(get_formatted_float(1.5), "1.5")
    
    def test_formatted_many_places(self):
        self.assertEqual(get_formatted_float(3.141594035), "3.1")
    
    def test_formatted_round_up(self):
        self.assertEqual(get_formatted_float(1.88), "1.9")
    
    def test_formatted_zero(self):
        self.assertEqual(get_formatted_float(0.0), "0")

    def test_transform_string(self):
        self.assertEqual(transform_string("fO -_oB_A- r___- "), "foobar")
