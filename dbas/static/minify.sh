#!/bin/bash

# @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
# Minimizes files with node's yuicompressor and appends them

# path of current file
path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# files which are minifed (has to be in the same order as paths!
files=($path"/js/compiled/main.min.js"
       $path"/js/compiled/main_discussion.min.js"
       $path"/js/compiled/main_ajax.min.js"
       $path"/js/compiled/main_review.min.js")

# path for files, which should be minified
paths=($path"/js/*.js"
       $path"/js/discussion/*.js"
       $path"/js/ajax/*.js"
       $path"/js/review/*.js")

# path for files, which should be appended for the final file
appends=($path"/js/compiled/main.min.js"
         $path"/js/compiled/main_discussion.min.js"
         $path"/js/socketio/socket.io-1.4.5.js"
         $path"/js/jquery/jquery.slimscroll-1.3.8.min.js"
         $path"/js/jquery/jquery-2.2.3.min.js"
         $path"/js/bootstrap/bootstrap-3.3.6.min.js"
         $path"/js/bootstrap/bootstrap-toggle.min.js")

final_file=$path"/js/compiled/dbas.min.js"
rm -f ${final_file};

mkdir -p $path"/js/compiled"

length=${#files[@]}
max_iter=$(expr $length - 1)
for i in `seq 0 $max_iter`;
    do
    rm -f ${files[i]}
    touch ${files[i]}

    old_size=$(find . -name "*.css" -ls | awk '{total += $7} END {print total}')
    old_size=$(expr $old_size / 1000)
    echo "Start compressing files with size" $old_size"K"

    for file in ${paths[i]}
        do if [ "$file" != "${files[i]}" ]; then
            if [[ "$file" != *'.min.js' && "$file" != 'socket.io-1.4.5.js' ]]; then
                echo "  Compressing" $file;
    	        java -jar ~/node_modules/yuicompressor/build/yuicompressor-2.4.8.jar $file >> ${files[i]};
    	    else
                echo "  Appending  " $file;
    	        cat  $file >> ${files[i]};
    	    fi
    	fi
    done

    new_size=$(du ${files[i]} | cut -f 1)
    save=$(expr $old_size - $new_size)
    echo "Finished ${files[i]} with" $new_size"K"
    echo "Saved" $save"K"
    echo ""
done

for j in `seq 0 $max_iter`;
    do
    for file in ${appends[j]}
        do
        echo "Appending" $file;
        cat $file >> ${final_file};
    done
done
echo ""
echo "Final size: " $(du ${final_file} | cut -f 1)"K"
