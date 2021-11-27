import numpy
import colormath.color_objects
import colormath.color_conversions


class Color:
    chromatic_adaptation_matrices = {
        'D50': {'X_n': 0.964212, 'Y_n': 1, 'Z_n': 0.825188},
        'D65': {'X_n': 0.950489, 'Y_n': 1, 'Z_n': 1.088840},
    }

    sRGB_to_XYZ_matrices = {
        'D50': numpy.array([[0.4360747, 0.3850649, 0.1430804], [0.2225045, 0.7168786, 0.0606169], [0.0139322, 0.0971045, 0.7141733]]),
        'D65': numpy.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]]),
    }

    sRGB_to_XYZ_matrices_reverse = {
        'D50': numpy.array([[3.1338561, -1.6168667, -0.4906146], [-0.9787684, 1.9161415, 0.0334540], [0.0719453, -0.2289914, 1.4052427]]),
        'D65': numpy.array([[3.2404542, -1.5371385, -0.4985314], [-0.9692660, 1.8760108, 0.0415560], [0.0556434, -0.2040259, 1.0572252]]),
    }

    def __init__(self, X:float, Y:float, Z:float, illuminant:str='D65'):
        self.X = X
        self.Y = Y
        self.Z = Z

        self.illuminant = illuminant
        self.observer = 2

    @property
    def X(self):
        return self.X

    @X.setter
    def X(self, X:float):
        if -3.1247467148632584 <= X <= 188.32848525706243:
            self._X = X
        else:
            raise ValueError(f'X out of range: {X}')

    @property
    def Y(self):
        return self.Y

    @X.setter
    def Y(self, Y:float):
        if 0 <= Y <= 100:
            self._Y = Y
        else:
            raise ValueError(f'Y out of range: {Y}')

    @property
    def Z(self):
        return self.Z

    @X.setter
    def Z(self, Z:float):
        if 0 <= Z <= 480.28122649600004:
            self._Z = Z
        else:
            raise ValueError(f'Z out of range: {Z}')

    @classmethod
    def from_XYZ(cls, X:float, Y:float, Z:float):
        return cls(X, Y, Z)

    @classmethod
    def from_Lab(cls, L:float, a:float, b:float, illuminant:str='D50'):
        if illuminant in cls.chromatic_adaptation_matrices.keys():
            X_n = cls.chromatic_adaptation_matrices[illuminant]['X_n']
            Y_n = cls.chromatic_adaptation_matrices[illuminant]['Y_n']
            Z_n = cls.chromatic_adaptation_matrices[illuminant]['Z_n']
        else:
            raise ValueError(f'illuminant out of range {{D50, D65}}: {illuminant}')

        def _inverse_f(t):
            delta = 6 / 29
            if t > delta:
                return t ** 3
            else:
                return 3 * delta ** 2 * (t - 4 / 29)

        if 0 <= L <= 100:
            X = X_n * _inverse_f((L + 16) / 116 + a / 500)
        else:
            raise ValueError(f'L out of range [0, 100]: {L}')
        if -128 <= a <= 128:
            Y = Y_n * _inverse_f((L + 16) / 116)
        else:
            raise ValueError(f'a out of range [-128, 128]: {a}')
        if -128 <= b <= 128:
            Z = Z_n * _inverse_f((L + 16) / 116 - b / 200)
        else:
            raise ValueError(f'b out of range [-128, 128]: {b}')

        return cls(X, Y, Z, illuminant)

    @classmethod
    def from_sRGB(cls, R:float, G:float, B:float, illuminant:str='D65'):
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

        if 0 <= R <= 1 and 0 <= G <= 1 and 0 <= B <= 1:
            C = numpy.array([_c_linear(R), _c_linear(G), _c_linear(B)])
            X, Y, Z = M.dot(C)
        else:
            raise ValueError(f'R or G or B out of range [0, 1]: {" ".join(map(str, [R, G, B]))}')

        return cls(numpy.round(X, 6), numpy.round(Y, 6), numpy.round(Z, 6), illuminant)

    def __repr__(self):
        return f'Color(X={self._X}, Y={self._Y}, Z={self._Z})'

    def get_Lab(self, format='tuple', illuminant:str='D50'):
        if illuminant in self.chromatic_adaptation_matrices.keys():
            X_n = self.chromatic_adaptation_matrices[illuminant]['X_n']
            Y_n = self.chromatic_adaptation_matrices[illuminant]['Y_n']
            Z_n = self.chromatic_adaptation_matrices[illuminant]['Z_n']
        else:
            raise ValueError(f'illuminant out of range {self.chromatic_adaptation_matrices.keys()}: {illuminant}')

        def _f(t):
            delta = 6 / 29
            if t > delta ** 3:
                return t ** (1 / 3)
            else:
                return t / (3 * delta ** 2) + (4 / 29)

        L = 116 * _f(self._Y / Y_n) - 16
        a = 500 * (_f(self._X / X_n) - _f(self._Y / Y_n))
        b = 200 * (_f(self._Y / Y_n) - _f(self._Z / Z_n))

        if format == 'tuple':
            return (L, a, b)
        else:
            raise ValueError(f'format out of range {{tuple}}: {format}')

    def get_sRGB(self, format='tuple', illuminant:str='D65'):
        if illuminant in self.sRGB_to_XYZ_matrices_reverse.keys():
            M = self.sRGB_to_XYZ_matrices_reverse[illuminant]
        else:
            raise ValueError(f'illuminant out of range {sRGB_to_XYZ_matrices.keys()}: {illuminant}')

        def _c_rgb(c_linear):
            if c_linear <= 0.0031308:
                return 12.92 * c_linear
            else:
                return ((1.055 * c_linear) ** (1 / 2.4)) - 0.055

        C = numpy.array([self._X, self._Y, self._Z])
        R, G, B = M.dot(C)

        if format == 'tuple':
            return (numpy.round(R, 6), numpy.round(G, 6), numpy.round(B, 6))
        else:
            raise ValueError(f'format out of range {{tuple}}: {format}')


if __name__ == '__main__':
    c = Color(1., 1., 1.)
    print(c.get_Lab())
