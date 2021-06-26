#! /bin/bash
cd ../result
files=$(ls *.pbs 2> /dev/null | wc -l)
if [ "$files" != "0" ]
    then
        rm *.pbs
fi
file=$(ls *.lsf 2> /dev/null | wc -l)
if [ "$file" != "0" ]
    then
        rm *.lsf
fi

