#!/bin/sh

repo_dir="`dirname $0`/.."
cd "$repo_dir"

original=original/spamsum
spamspy=spamsum/spamsum.py

target_files="original/spamsum.c LICENSE README.md tests/data/*"


(cd original/; make)

for target_file in $target_files; do
    echo -n "Comparing $target_file - "

    original_out=`$original $target_file`
    spamspy_out=`$spamspy $target_file`

    if [ "$original_out" = "$spamspy_out" ]; then
        echo "OK"
    else
        echo "differ"
        return 1
    fi
done
