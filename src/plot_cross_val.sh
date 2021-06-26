#! /bin/bash
cd ../result
MAXINDEX=`ls chr*.py |wc -l`
File=`ls *.model 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
    File=`ls *.model 2>/dev/null |wc -w`
    sleep 10
done
if [ $File = ${MAXINDEX} ]
    then
        python ../src/plot_cross_val.py -d $1
fi
