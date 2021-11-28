import numpy
import colormath.color_objects
import colormath.color_conversions


class Color:
    chromatic_adaptation_matrices = {
        '2': {
            'D50': {'X_n': 0.964212, 'Y_n': 1, 'Z_n': 0.825188},
            'D65': {'X_n': 0.950489, 'Y_n': 1, 'Z_n': 1.088840},
        },
    }

    sRGB_to_XYZ_matrices = {
        'D50': numpy.array([[0.4360747, 0.3850649, 0.1430804], [0.2225045, 0.7168786, 0.0606169], [0.0139322, 0.0971045, 0.7141733]]),
        'D65': numpy.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]]),
    }

    sRGB_to_XYZ_matrices_reverse = {
        'D50': numpy.array([[3.1338561, -1.6168667, -0.4906146], [-0.9787684, 1.9161415, 0.0334540], [0.0719453, -0.2289914, 1.4052427]]),
        'D65': numpy.array([[3.2404542, -1.5371385, -0.4985314], [-0.9692660, 1.8760108, 0.0415560], [0.0556434, -0.2040259, 1.0572252]]),
    }

    def __init__(self, X:float, Y:float, Z:float, illuminant:str='D65', observer:str='2'):
        self.X = X
        self.Y = Y
        self.Z = Z

        self.illuminant = illuminant
        self.observer = observer

    @property
    def X(self):
        return self.X

    @X.setter
    def X(self, X:float):
        self._X = X

    @property
    def Y(self):
        return self.Y

    @X.setter
    def Y(self, Y:float):
        self._Y = Y

    @property
    def Z(self):
        return self.Z

    @X.setter
    def Z(self, Z:float):
        self._Z = Z

    @classmethod
    def from_XYZ(cls, X:float, Y:float, Z:float, illuminant:str='D65', observer:str='2'):
        return cls(X, Y, Z, illuminant, observer)

    @classmethod
    def from_Lab(cls, L:float, a:float, b:float, illuminant:str='D65', observer:str='2'):
        if illuminant in cls.chromatic_adaptation_matrices[observer].keys():
            X_n = cls.chromatic_adaptation_matrices[observer][illuminant]['X_n']
            Y_n = cls.chromatic_adaptation_matrices[observer][illuminant]['Y_n']
            Z_n = cls.chromatic_adaptation_matrices[observer][illuminant]['Z_n']
        else:
            raise ValueError(f'illuminant out of range {cls.chromatic_adaptation_matrices[observer].keys()}: {illuminant}')

        epsilon = 216 / 24389
        kappa = 24389 / 27

        L_n = L * 100
        f_y = (L_n + 16) / 116
        a_n = (a - 0.5) * 256
        f_x = a_n / 500 + f_y
        b_n = (b - 0.5) * 256
        f_z = f_y - b_n / 200

        x = f_x ** 3 if f_x ** 3 > epsilon else (116 * f_x - 16) / kappa
        X = X_n * x

        y = ((L_n + 16) / 116) ** 3 if L_n > kappa * epsilon else L_n / kappa
        Y = Y_n * y

        z = f_z ** 3 if f_z ** 3 > epsilon else (116 * f_z - 16) / kappa
        Z = Z_n * z

        return cls(X, Y, Z, illuminant, observer)

    @classmethod
    def from_sRGB(cls, R:float, G:float, B:float, illuminant:str='D65', observer:str='2'):
        if illuminant in cls.sRGB_to_XYZ_matrices.keys():
            M = cls.sRGB_to_XYZ_matrices[illuminant]
        else:
            raise ValueError(f'illuminant out of range {sRGB_to_XYZ_matrices.keys()}: {illuminant}')

        def _c_linear(c_rgb):
            # calculate gamma-expanded values
            if c_rgb <= 0.04045:
                return c_rgb / 12.92
            else:
                return ((c_rgb + 0.055) / 1.055) ** 2.4

        C = numpy.array([_c_linear(R), _c_linear(G), _c_linear(B)])
        X, Y, Z = M.dot(C)
        
        return cls(X, Y, Z, illuminant, observer)

    def __repr__(self):
        return f'Color(X={self._X}, Y={self._Y}, Z={self._Z})'

    def get_Lab(self, format='tuple'):
        X_n = self.chromatic_adaptation_matrices[self.observer][self.illuminant]['X_n']
        Y_n = self.chromatic_adaptation_matrices[self.observer][self.illuminant]['Y_n']
        Z_n = self.chromatic_adaptation_matrices[self.observer][self.illuminant]['Z_n']
        
        def _f(t):
            epsilon = 216 / 24389
            kappa = 24389 / 27
            if t > epsilon:
                return t ** (1 / 3)
            else:
                return ((t * kappa) + 16) / 116

        L = 116 * _f(self._Y / Y_n) - 16
        a = 500 * (_f(self._X / X_n) - _f(self._Y / Y_n))
        b = 200 * (_f(self._Y / Y_n) - _f(self._Z / Z_n))

        if format == 'tuple':
            return (L / 100, (a + 128) / 256, (b + 128) / 256)
        elif format == 'tuple_upscale':
            return (L, a, b)
        else:
            raise ValueError(f'format out of range {{tuple, tuple_upscale}}: {format}')

    def get_sRGB(self, format='tuple'):
        M = self.sRGB_to_XYZ_matrices_reverse[self.illuminant]
        
        def _c_rgb(c_linear):
            if c_linear <= 0.0031308:
                return 12.92 * c_linear
            else:
                return ((1.055 * c_linear) ** (1 / 2.4)) - 0.055

        C = numpy.array([self._X, self._Y, self._Z])
        R, G, B = M.dot(C)

        def _c_rgb(c_linear):
            # calculate gamma-expanded values
            if c_linear <= 0.0031308:
                return c_linear * 12.92
            else:
                return (1.055 * (c_linear ** (1 / 2.4))) - 0.055

        if format == 'tuple':
            return (_c_rgb(R), _c_rgb(G), _c_rgb(B))
        else:
            raise ValueError(f'format out of range {{tuple}}: {format}')


if __name__ == '__main__':
    a = Color.from_sRGB(1.0115059552563181, 0.9870652513165344, 1.1020986165231543, illuminant='D50')
    print(a)
    print(a.get_sRGB())
    a = Color.from_sRGB(1.085157, 0.976922, 0.958809, illuminant='D65')
    print(a)
    print(a.get_sRGB())
    quit()

    for x in [(0, 0, 0), (1, 1, 1)]:
        a = Color(*x, illuminant='D50')
        print(a)
        print(a.get_Lab(format='tuple_upscale'))
        print(a.get_sRGB())

        b = colormath.color_objects.XYZColor(*x)
        print(b)
        b_Lab = colormath.color_conversions.convert_color(b, colormath.color_objects.LabColor, target_illuminant='d65')
        print(b_Lab)
        b_sRGB = colormath.color_conversions.convert_color(b, colormath.color_objects.sRGBColor)
        print(b_sRGB)
        print('---')

    
