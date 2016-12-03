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

# path for files, which should be minimized
paths=($path"/js/*.js"
       $path"/js/discussion/*.js"
       $path"/js/ajax/*.js"
       $path"/js/review/*.js")

# path for files, which should be appended for the final file
appends=($path"/js/min/main_ajax.min.js"
         $path"/js/min/main.min.js"
         $path"/js/min/main_discussion.min.js"
         $path"/js/min/main_review.min.js"
         )

final_file=$path"/js/compiled/dbas.min.js"
rm -f ${final_file};

mkdir -p $path"/js/min"

# minimize
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
            if [[ "$file" != *'.min.js' ]]; then
                echo "  Compressing" $file;
    	        java -jar ~/node_modules/yuicompressor/build/2-2.4.8.jar $file >> ${files[i]};
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

# append
for j in `seq 0 $max_iter`;
    do
    for file in ${appends[j]}
        do
        echo "Appending" $file;
        cat $file >> ${final_file};
    done
done

#tidy up
for i in `seq 0 $max_iter`;
    do
    rm -f ${files[i]}
done

echo ""
echo "Final size: " $(du ${final_file} | cut -f 1)"K"
