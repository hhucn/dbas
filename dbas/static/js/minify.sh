#!/usr/bin/env bash

# @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>

# path of current file
path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
file="/dbas.min.js"

# create path for final file
final_file=$path$file
# remove old file
[ -e $final_file ] && rm $final_file
# create final file
google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE $path"/"{main,ajax,discussion,review}/*.js > $final_file
