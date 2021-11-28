import numpy
import colormath.color_objects
import colormath.color_conversions
import colormath.color_diff

import color

def difference(color_a, color_b, mode='Delta E (CIE 1976)', substrate='graphic arts'):
    if mode == 'Delta E (CIE 1976)':
        return numpy.sum((color_a.get_Lab(format='numpy_upscale') - color_b.get_Lab(format='numpy_upscale')) ** 2) ** 0.5
    elif mode == 'Delta E (CIE 1994)':
        if substrate == 'graphic arts':
            K_L = 1
            K_1 = 0.045
            K_2 = 0.015
        elif substrate == 'textile':
            K_L = 2
            K_1 = 0.048
            K_2 = 0.014
        else:
            raise ValueError(f'substrate out of range {{graphic arts, textile}}: {substrate}')
            
        a_L, a_a, a_b = color_a.get_Lab(format='tuple_upscale')
        b_L, b_a, b_b = color_b.get_Lab(format='tuple_upscale')
        dL = (a_L - b_L) ** 2
        a_C = (a_a ** 2 + a_b ** 2) ** 0.5
        b_C = (b_a ** 2 + b_b ** 2) ** 0.5
        dC = (a_C - b_C) ** 2
        dH = (a_a - b_a) ** 2 + (a_b - b_b) ** 2 - dC
        S_L = 1
        S_C = 1 + K_1 * a_C
        S_H = 1 + K_2 * a_C
        K_C = 1
        K_H = 1

        return ((dL / (K_L * S_L) ** 2) + (dC / (K_C * S_C) ** 2) + (dH / (K_H * S_H) ** 2)) ** 0.5
    else:
        raise ValueError(f'mode out of range {{Delta E (CIE 1976), Delta E (CIE 1994)}}: {mode}')


if __name__ == '__main__':
    a = color.Color(1, 1, 1, illuminant='D50')
    c  = color.Color(0, 0, 0, illuminant='D50')
    print(a.get_Lab(format='tuple_upscale'))
    print(difference(a, a, mode='Delta E (CIE 1994)'))
    print(difference(a, c, mode='Delta E (CIE 1994)'))

    b = colormath.color_objects.XYZColor(1, 1, 1)
    b_Lab = colormath.color_conversions.convert_color(b, colormath.color_objects.LabColor)
    print(b_Lab)
    d = colormath.color_objects.XYZColor(0, 0, 0)
    d_Lab = colormath.color_conversions.convert_color(d, colormath.color_objects.LabColor)
    print(colormath.color_diff.delta_e_cie1994(b_Lab, b_Lab))
    print(colormath.color_diff.delta_e_cie1994(b_Lab, d_Lab))