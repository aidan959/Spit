#!/bin/sh

set -xe

for FILE in tests/*; do cat $FILE | python3 spit.py; done
