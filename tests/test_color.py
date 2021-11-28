import unittest

import pycoli.color

class ColorTest(unittest.TestCase):
    def test_Lab_XYZ_conversion(self):
        for illuminant in ['D50', 'D65']:
            for input_Lab_color in [(0, 0, 0), (1, 1, 1)]:
                c = pycoli.color.Color.from_Lab(*input_Lab_color, illuminant=illuminant)
                for a, b in zip(input_Lab_color, c.get_Lab()):
                    self.assertAlmostEqual(a, b)


    def test_sRGB_XYZ_conversion(self):
        for illuminant in ['D50', 'D65']:
            for input_sRGB_color in [(0, 0, 0), (1, 1, 1)]:
                c = pycoli.color.Color.from_sRGB(*input_sRGB_color, illuminant=illuminant)
                for a, b in zip(input_sRGB_color, c.get_sRGB()):
                    self.assertAlmostEqual(a, b, places=6)


    def test_Lab_sRGB_conversion(self):
        input_Lab_color = (1, 1, 1)
        c_from_Lab = pycoli.color.Color.from_Lab(*input_Lab_color)
        output_sRGB_color = c_from_Lab.get_sRGB()
        c_from_sRGB = pycoli.color.Color.from_sRGB(*output_sRGB_color)
        for a, b in zip(input_Lab_color, c_from_Lab.get_Lab()):
            self.assertAlmostEqual(a, b)
