#!/bin/sh
repo_dir="`dirname $0`/.."
repo_dir=`readlink -f "$repo_dir"`
ngram="$repo_dir/spamspy/ngram.py"

cd "$repo_dir/tests/data"

all_files="*.txt"

for target_file in $all_files; do
    echo -n "verify $target_file - "

    echo -n "update db - "
    rm -f registry.dat

    for other_file in $all_files; do
        if [ $other_file != $target_file ]; then
            $ngram update $other_file
        fi
    done

    echo -n "search - "
    search_out=`$ngram search $target_file`

    case "$target_file" in
        lorem_*)
            match=`echo "$search_out" | grep 'lorem.*, [0-9]\{2\}'`
            ;;
        pieces_*)
            match=`echo "$search_out" | grep 'pieces.*, [0-9]\{2\}'`
            ;;
        random_*)
            match=`echo "$search_out" | grep 'None, 0'`
            ;;
        *)
            echo "FAIL"
            echo "error: unknown file $target_file"
            exit 1
            ;;
    esac

    if [ -z "$match" ]; then
        echo "FAIL"
        echo "error: $search_out"
        exit 1
    else
        echo "OK"
    fi
done

rm -f registry.dat
