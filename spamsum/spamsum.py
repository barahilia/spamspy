#!/usr/bin/env python
from sys import argv
from string import ascii_lowercase, ascii_uppercase, digits


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
        return h & 0xFFFFFFFF

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


def _spamsum(s, block_size):
    # XXX consider making vars below be state of an object; use wrapper function
    yielded = 0
    sh = SumHash()
    rh = RollingHash()

    for c in s:
        sh.update(c)
        rh.update(c)

        if (rh.hash % block_size) == (block_size - 1):
            if yielded < 64 - 1:
                yield sh.hash
                yielded += 1
                sh = SumHash()

    if rh.hash != 0:
        # XXX conforming; but this is not needed if hash was just yielded
        yield sh.hash


def _block_size(s):
    block_size = 3  # mimimal block size
    max_hash_length = 64

    while block_size * max_hash_length < len(s):
        block_size *= 2

    return block_size


def spamsum(s, block_size=None):
    b64 = ascii_uppercase + ascii_lowercase + digits + '+/'

    block_size = block_size or _block_size(s)
    hashes = _spamsum(s, block_size)

    # XXX if len(hashes) < 32 and block is not minimal - repeat for halved block
    return ''.join(b64[h % 64] for h in hashes)


def main():
    path = argv[1]
    s = open(path).read()

    block_size = _block_size(s)

    normal = spamsum(s, block_size)
    shorter = spamsum(s, block_size * 2)

    print '%d:%s:%s' % (block_size, normal, shorter)


if __name__ == '__main__':
    main()
