#! /bin/bash
cd ../result
MAXINDEX=`ls *.py |wc -l`
File=`ls *_predict_trains.txt 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
    File=`ls *_predict_trains.txt 2>/dev/null |wc -w`
    sleep 200
done
if [ $File = ${MAXINDEX} ]
    then
        python ../src/cat_add_feature_predict.py -d ${1} -o ${2}
fi
