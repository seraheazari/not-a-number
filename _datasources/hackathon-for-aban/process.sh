#!/usr/bin/env sh

cd $(dirname $(readlink -f $0))
mkdir -p work && cd work

../read-round-1-data.py ../src/bloodynovember-sample-victims-data.xlsx \
                        ../../../_data/bloody-november \
                        --create-posts
