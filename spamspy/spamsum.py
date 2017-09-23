#!/usr/bin/env python
from sys import argv
from string import ascii_lowercase, ascii_uppercase, digits

from params import get_params

MAX_DIGEST_LEN = 64
MIN_BLOCK_LEN = 3

MAX_UINT32 = 0xFFFFFFFF


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
        return h & MAX_UINT32

    def update(self, c):
        c = ord(c)

        self.h2 -= self.h1
        self.h2 += self._ROLLING_WINDOW * c

        self.h1 += c
        self.h1 -= self.window[self.n % self._ROLLING_WINDOW]

        self.window[self.n % self._ROLLING_WINDOW] = c
        self.n += 1

        self.h3 = (self.h3 << 5) & MAX_UINT32
        self.h3 ^= c


class SumHash:
    def __init__(self):
        self.hash = 0x28021967

    def update(self, c):
        self.hash *= 0x01000193
        self.hash &= MAX_UINT32
        self.hash ^= ord(c)


def _spamsum(s, block_len, digest_len, legacy_mode):
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
        # No need to yield initial hash, unless mimicing the original
        if legacy_mode or sh.hash != SumHash().hash:
            yield sh.hash


def _block_len(s):
    block_len = MIN_BLOCK_LEN

    while block_len * MAX_DIGEST_LEN < len(s):
        block_len *= 2

    return block_len


def spamsum(s, block_len=None, digest_len=MAX_DIGEST_LEN, legacy_mode=False):
    b64 = ascii_uppercase + ascii_lowercase + digits + '+/'

    block_len = block_len or _block_len(s)
    hashes = _spamsum(s, block_len, digest_len, legacy_mode)

    return ''.join(b64[h % 64] for h in hashes)


def full_spamsum(file_to_hash):
    s = open(file_to_hash).read()

    block_len = _block_len(s)

    while True:
        normal = spamsum(s, block_len, MAX_DIGEST_LEN)
        shorter = spamsum(s, block_len * 2, MAX_DIGEST_LEN / 2)

        normal_should_be_longer = len(normal) < (MAX_DIGEST_LEN / 2)
        can_reduce_block = block_len > MIN_BLOCK_LEN

        if normal_should_be_longer and can_reduce_block:
            block_len /= 2
        else:
            return '%d:%s:%s' % (block_len, normal, shorter)


def hash_split(full_hash):
    block_len, normal, shorter = full_hash.split(':')
    return int(block_len), normal, shorter


def hashes_match(hash1, hash2):
    block_len_1, normal_1, shorter_1 = hash_split(hash1)
    block_len_2, normal_2, shorter_2 = hash_split(hash2)

    if block_len_1 == block_len_2:
        return spamsum_match(normal_1, normal_2)
    elif block_len_1 * 2 == block_len_2:
        return spamsum_match(shorter_1, normal_2)
    elif block_len_1 == block_len_2 * 2:
        return spamsum_match(normal_1, shorter_2)

    return False


def search_db(dbname, spamsum_hash):
    for line in open(dbname):
        db_hash = line.strip()

        if hashes_match(db_hash, spamsum_hash):
            return db_hash


def main():
    params = get_params()

    if params.dbname is not None:
        spamsum_hash = full_spamsum(params.file_to_search)
        print search_db(params.dbname, spamsum_hash)
    else:
        print full_spamsum(params.file_to_hash)


if __name__ == '__main__':
    main()
