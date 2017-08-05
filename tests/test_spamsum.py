#!/usr/bin/python
from unittest import TestCase, main
from context import spamsum
from spamsum.edit_dist import Costs, edit_dist
from spamsum.spamsum import RollingHash, SumHash, spamsum


class SimpleInsertDelete(TestCase):
    def check(self, a, b, d):
        self.assertEqual(edit_dist(a, b), d)

    def test_empty_case(self):
        self.check('', '', 0)

    def test_deletion(self):
        self.check('a', '', 1)

    def test_long_str_deletion(self):
        self.check('abcd', 'abc', 1)

    def test_replacement(self):
        self.check('a', 'b', 2)

    def test_suffix_replacement(self):
        self.check('aa', 'ab', 2)

    def test_internal_insert(self):
        self.check('aabb', 'aaabb', 1)

    def test_complex_change(self):
        self.check('xyz', 'ayzb', 3)

    def test_swap(self):
        self.check('ab', 'ba', 2)


class SpamsumDistance(TestCase):
    """Set weights as in spamsum README and code

    The code has 2 versions of costs. One that is the default and is set with
    TRN_SPEEDUP macro has change and swap weights of 3 and 5 and they are
    simply not used.
    """
    def check(self, a, b, d):
        costs = Costs()
        costs.change = 3
        costs.swap = 5

        dist = edit_dist(a, b, costs)
        self.assertEqual(dist, d)

    def test_change_start(self):
        self.check('abc', 'dbc', 2)

    def test_change_middle(self):
        self.check('aabxy', 'aadxy', 2)

    def test_change_end(self):
        self.check('abc', 'abd', 2)

    def test_swap_start(self):
        self.check('abc', 'bac', 2)

    def test_swap_middle(self):
        self.check('aabxy', 'abaxy', 2)


class SmallCosts(TestCase):
    """Set small costs for change and swap

    They appear in the optional version in spamsum code. If used, they will
    make difference and cause distance to be smaller.
    """
    def check(self, a, b, d):
        costs = Costs()
        costs.change = 1
        costs.swap = 1

        dist = edit_dist(a, b, costs)
        self.assertEqual(dist, d)

    def test_change_start(self):
        self.check('abc', 'dbc', 1)

    def test_swap_middle(self):
        self.check('aabxy', 'abaxy', 1)


class HashTestBase(TestCase):
    def hash(self, s):
        h = self.HashClass()

        for c in s:
            h.update(c)

        return h.hash


class RollingHashTest(HashTestBase):
    HashClass = RollingHash

    def test_init(self):
        self.assertEqual(self.hash(''), 0)

    def test_update(self):
        c = ord('a')
        h1 = c
        h2 = 7 * c
        h3 = (0 << 5) ^ c

        self.assertEqual(self.hash('a'), h1 + h2 + h3)

    def test_update_twice(self):
        c = ord('a')
        h1 = c
        h2 = 7 * c
        h3 = (0 << 5) ^ c

        c = ord('b')
        h2 += 7 * c - h1
        h1 += c
        h3 = (h3 << 5) ^ c

        self.assertEqual(self.hash('ab'), h1 + h2 + h3)

    def test_hash_is_signed_int_32(self):
        self.assertLess(self.hash('abcdefg'), 0x7FFFFFFF)

    def test_only_last_7_chars_matter(self):
        s = 'abcdefg'
        self.assertEqual(self.hash(s), self.hash('xyz' + s))


class SumHashTest(HashTestBase):
    HashClass = SumHash

    def test_init(self):
        self.assertEqual(self.hash(''), 671226215)

    def test_single_char(self):
        h = 671226215
        h *= 16777619
        h ^= ord('a')

        self.assertEqual(self.hash('a'), h % (1 << 32))

    def test_two_chars(self):
        h = 671226215

        h *= 16777619
        h ^= ord('a')

        h *= 16777619
        h ^= ord('b')

        self.assertEqual(self.hash('ab'), h % (1 << 32))


class SpamsumTest(TestCase):
    def test_empty(self):
        self.assertEqual(spamsum(''), '')

    def test_single_char(self):
        self.assertEqual(spamsum('a'), 'E')

    def test_two_chars_single_out(self):
        self.assertEqual(spamsum('ba'), 'k')


if __name__ == '__main__':
    main()
