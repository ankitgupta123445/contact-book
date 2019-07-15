import unittest
from kernel.models.validator import *


class TestTestData(unittest.TestCase):
    def test_check_email_valid(self):
        """
        Tests that all check email
        """
        self.assertIsNone(check_email("example@jay.com"))

    def test_check_email_invalid(self):
        """
        Tests that all check email
        """
        with self.assertRaises(TypeError):
            check_email("example@jay.com@.com")

    def test_check_mobile_valid(self):
        """
        Tests that all check email
        """
        self.assertIsNone(check_mobile("7795540204"))

    def test_check_mobile_invalid(self):
        """
        Tests that all check email
        """
        with self.assertRaises(TypeError):
            check_email("1234567890")


if __name__ == '__main__':
    unittest.main()
