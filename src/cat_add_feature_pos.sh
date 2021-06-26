#! /bin/bash
cd ../result
MAXINDEX=`ls *.py |wc -l`
File=`ls *_pos_trains.txt 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
    File=`ls *_pos_trains.txt 2>/dev/null |wc -w`
    sleep 10
done
if [ $File = ${MAXINDEX} ]
    then
        python ../src/cat_add_feature_pos.py -d ${1} -o ${2}
fi
