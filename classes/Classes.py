from struct import pack


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Color:
    def __init__(self, R, G, B, A):
        self.R = R
        self.G = G
        self.B = B
        self.A = A


def f2b(num):
    return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in pack('!f', num))