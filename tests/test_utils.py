import unittest

import pycoli.color
import pycoli.utils


class UtilsTest(unittest.TestCase):
    def test_difference(self):
        color_a = pycoli.color.Color(1, 1, 1)
        self.assertEqual(pycoli.utils.difference(color_a, color_a), 0)