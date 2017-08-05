from string import ascii_lowercase, ascii_uppercase, digits


def make_signed_int32(n):
    all_ones =     0xFFFFFFFF
    max_positive = 0x7FFFFFFF

    n &= all_ones

    if n <= max_positive:
        return n
    else:
        return -1 - (all_ones ^ n)


class RollingHash:
    _ROLLING_WINDOW = 7

    def __init__(self):
        self.h1 = 0
        self.h2 = 0
        self.h3 = 0

        self.window = [0] * self._ROLLING_WINDOW
        self.n = 0

    @property
    def hash(self):
        h = self.h1 + self.h2 + self.h3
        return make_signed_int32(h)

    def update(self, c):
        c = ord(c)

        self.h2 -= self.h1
        self.h2 += self._ROLLING_WINDOW * c

        self.h1 += c
        self.h1 -= self.window[self.n % self._ROLLING_WINDOW]

        self.window[self.n % self._ROLLING_WINDOW] = c
        self.n += 1

        self.h3 = (self.h3 << 5) & 0xFFFFFFFF
        self.h3 ^= c


class SumHash:
    def __init__(self):
        self.hash = 0x28021967

    def update(self, c):
        self.hash *= 0x01000193
        self.hash &= 0xFFFFFFFF
        self.hash ^= ord(c)


def spamsum(s):
    # XXX drop this after rolling hash is being used too
    if not s:
        return ''

    b64 = ascii_uppercase + ascii_lowercase + digits + '+/'
    h = SumHash()

    for c in s:
        h.update(c)

    return b64[h.hash % 64]
