import colormath.color_objects
import colormath.color_conversions


class Color:
    illuminants = {
        'D50': {'X_n': 96.4212, 'Y_n': 100, 'Z_n':  82.5188},
        'D65': {'X_n': 95.0489, 'Y_n': 100, 'Z_n': 108.8840},
    }

    def __init__(self, X:float, Y:float, Z:float, illuminant:str='D65'):
        self.X = X
        self.Y = Y
        self.Z = Z

        self.illuminant = illuminant

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
        if illuminant in cls.illuminants.keys():
            X_n = cls.illuminants[illuminant]['X_n']
            Y_n = cls.illuminants[illuminant]['Y_n']
            Z_n = cls.illuminants[illuminant]['Z_n']
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
        if illuminant in cls.illuminants.keys():
            X_n = cls.illuminants[illuminant]['X_n']
            Y_n = cls.illuminants[illuminant]['Y_n']
            Z_n = cls.illuminants[illuminant]['Z_n']
        else:
            raise ValueError(f'illuminant out of range {{D65}}: {illuminant}')


    def __repr__(self):
        return f'Color(X={self._X}, Y={self._Y}, Z={self._Z})'

    def get_Lab(self, format='tuple', illuminant:str='D50'):
        if illuminant in self.illuminants.keys():
            X_n = self.illuminants[illuminant]['X_n']
            Y_n = self.illuminants[illuminant]['Y_n']
            Z_n = self.illuminants[illuminant]['Z_n']
        else:
            raise ValueError(f'illuminant out of range {{D50, D65}}: {illuminant}')

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

    def get_sRGB(self, format='tuple', illuminant:str='D50'):
        pass



if __name__ == '__main__':
    c = Color.from_XYZ(1.0, 0.9, 0.8)
    d = Color.from_Lab(100, -128, -128)
    print(d)
    e = colormath.color_objects.LabColor(100, -128, -128)
    print(e)
    print(d.get_Lab())
    f = colormath.color_conversions.convert_color(e, colormath.color_objects.XYZColor)
    print(f)
