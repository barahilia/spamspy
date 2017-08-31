from collections import Counter, defaultdict
from itertools import chain
from spamsum import spamsum

BLOCK_LEN = 1000
NGRAM_LEN = 5

registry = defaultdict(set)  # ngram -> {source...}


def get_digest(s):
    return spamsum(s, block_len=BLOCK_LEN)


def _ngrams(s):
    for i in range(len(s) - NGRAM_LEN + 1):
        yield s[i: i + NGRAM_LEN]


def update_registry(digest, source):
    for ngram in _ngrams(digest):
        registry[ngram].append(source)


def find_best_match(digest):
    sources = chain.from_iterable(registry[ngram] for ngram in _ngrams(digest))
    counter = Counter(sources)
    most_common_source, = counter.most_common(1)
    source, frequency = most_common_source
    return source, frequency
