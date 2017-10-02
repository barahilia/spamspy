*******
spamspy
*******

.. image:: https://travis-ci.org/barahilia/spamspy.svg?branch=master
    :target: https://travis-ci.org/barahilia/spamspy
    :alt: Build status

Pure Python implementation of *spamsum* (also known from *ssdeep*) with improvements and extensions.

Introduction
============

Conventional hash and checksum tools like
`sha256 <https://en.m.wikipedia.org/wiki/SHA-2>`_ and
`CRC32 <https://en.m.wikipedia.org/wiki/Cyclic_redundancy_check>`_
are good at grasping **exact** file content.
They result in very different hash after any byte or even bit change.
`Spamsum <https://www.samba.org/ftp/unpacked/junkcode/spamsum/README>`_
was developed by Andrew Tridgell to compare **similar** files.
After several changes in few parts of a file hash changes only slightly.
Spamsum comes in two parts: a "fuzzy" hash generating similar output for similar files,
and a slightly adopted edit distance implementation to estimate how similar the hashes
and their files are.

Spamsum hash length is bound by 64 characters. Block size is chosen at about 1/64 of the
file size. Every block is hashed to one character. File division to blocks depends on
file content so that on average block size will be like the
target. This allows to get same blocks with same one-character hash even if other parts of the files are different.

* comparable files should be up to two times in size one from another, due to block size
* for the same reason you can **not** use spamsum to search for some large chunk appearance in files
* all 64 blocks might appear in the beginning and spamsum hash might "cover" only the first part of the file
* you should consider file format before usage; zip archives to be decompressed before hashing
* this hash is **not** secure and does **not** garantee similarity; it should be easy enough to generate
  file having specific hash

Spamspy
=======

In this project both spamsum components - hash and edit distance, - are implemented in pure Python. As well
a number of improvements are made. Spamsum hash length limitation is dropped, and so both block length and
the maximal hash length are configurable and can depend on the file size.

Another system for library search based on ngrams is introduced. Given a large library of files and one
new file we want to check if any large part from the new file appears in the library. For this all files
are hashed with spamsum with some constant block size. Then hashes are split to ngrams. Library preserves
a mapping from ngram to its original files. Search in library iterates over all ngrams of the new file hash
and yields the library file(s) with most matches. Assuming block size of 10KB and ngram size of 5, single
match means some chance of about 50KB match in the files themselves.

Usage
=====

The package depends on standard modules only. Install with::

    pip install spamspy

In code:

.. code-block:: python

    from spamspy.spamsum import spamsum
    s1 = 'some long text'  # or open('first.txt').read()
    hash1 = spamsum(s1)
    hash2 = spamsum('somewhat long telegram')

    from spamsum.edit_dist import edit_dist

    ed = edit_dist(hash1, hash2)  # large number means more difference

In shell:

.. code-block:: sh

    spamsum first.txt  # 3:uqHRXLAHBn:K2
    edit_dist uqHRXLAHBn uqHRXLAHc  # 2 - two changes from first hash to the second

    ngram_spy update first.txt  # hashes and saves ngrams in ./registry.dat
    ngram_spy search second.txt # (first.txt, 23) - matches on 23 ngrams
    ngram_spy search other.txt  # (None, 0) - no matches found

Performance
===========

In Python 2.7 spamsum runs about 600 times slower than the native implementation.
The good news is that in PyPy 5.1.1 it is only 15 times slower than the native which should be
tolerable in many applications. This would be the price for extensions, the new ngrams
algorithm and for convenience of in-Python world. If blazing speed is the must, then
the new code should be ported back.

License
=======

Copyright (c) 2017 Ilia Barahovsky

This project is distributed under MIT License.

The *spamsum* algorithm and tool was developed by Andrew Tridgell as an
efficient similarity comparison between two files and a spam filter for mail
client. It is licensed under the GNU General Public License version 2 or under
the terms of the Perl Artistic license. It was copied without modifications from
https://www.samba.org/ftp/unpacked/junkcode/spamsum/ to ``original/`` for
verification of the Python port.
