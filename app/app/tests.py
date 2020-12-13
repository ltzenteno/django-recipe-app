from django.test import TestCase
from app.calc import subtract


class CalcTests(TestCase):

    def test_subtract_numbers(self):
        """Test that values are subsracted and returned"""
        self.assertEqual(subtract(5, 11), 6)