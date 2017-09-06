#!/bin/sh

cd tests/data
a="*.txt"

for b in $a; do
    echo -n "searching $b: ... "
    rm -f registry.dat
    for c in $a; do
        if [ $b != $c ]; then
            ../../spamsum/ngram.py u $c
        fi
    done
    ../../spamsum/ngram.py s $b
done

rm -f registry.dat
