import unittest

import pycoli.color

class ColorTest(unittest.TestCase):
    def test_Lab_XYZ_conversion(self):
        input_Lab_color = (100., 128., 128.)
        c = pycoli.color.Color.from_Lab(*input_Lab_color)
        self.assertTupleEqual(input_Lab_color, c.get_Lab())


    def test_Lab_sRGB_conversion(self):
        input_Lab_color = (100., 128., 128.)
        c_from_Lab = pycoli.color.Color.from_Lab(*input_Lab_color)
        output_sRGB_color = c_from_Lab.get_sRGB()
        print(output_sRGB_color)
        c_from_sRGB = pycoli.color.Color.from_sRGB(*output_sRGB_color)
        self.assertTupleEqual(input_Lab_color, c.get_Lab())
