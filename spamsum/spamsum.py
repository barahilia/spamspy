#!/usr/bin/env python
from sys import argv
from string import ascii_lowercase, ascii_uppercase, digits

MAX_DIGEST_LEN = 64
MIN_BLOCK_LEN = 3


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


def _spamsum(s, block_len, digest_len):
    yielded = 0
    sh = SumHash()
    rh = RollingHash()

    for c in s:
        sh.update(c)
        rh.update(c)

        if (rh.hash % block_len) == (block_len - 1):
            if yielded < (digest_len - 1):
                yield sh.hash
                yielded += 1
                sh = SumHash()

    if rh.hash != 0:
        # XXX conforming; but this is not needed if hash was just yielded
        yield sh.hash


def _block_len(s):
    block_len = MIN_BLOCK_LEN

    while block_len * MAX_DIGEST_LEN < len(s):
        block_len *= 2

    return block_len


def spamsum(s, block_len=None, digest_len=MAX_DIGEST_LEN):
    b64 = ascii_uppercase + ascii_lowercase + digits + '+/'

    block_len = block_len or _block_len(s)
    hashes = _spamsum(s, block_len, digest_len)

    return ''.join(b64[h % 64] for h in hashes)


def main():
    path = argv[1]
    s = open(path).read()

    block_len = _block_len(s)

    while True:
        normal = spamsum(s, block_len)
        shorter = spamsum(s, block_len * 2)

        normal_should_be_longer = len(normal) < (MAX_DIGEST_LEN / 2)
        can_reduce_block = block_len > MIN_BLOCK_LEN

        if normal_should_be_longer and can_reduce_block:
            block_len /= 2
        else:
            print '%d:%s:%s' % (block_len, normal, shorter)
            return


if __name__ == '__main__':
    main()
