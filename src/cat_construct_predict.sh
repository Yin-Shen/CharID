#! /bin/bash
cd ../result
MAXINDEX=`find . -name "chr*.py" |wc -l`
File=`ls chr*_predict.txt 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
    File=`ls chr*_predict.txt 2>/dev/null |wc -w`
    sleep 200
done
if [ $File = ${MAXINDEX} ]
    then
        for i in `ls chr*_predict.txt|sort -V`
        do
            echo "File name is: $i";
            cat $i >> whole_predict.bed;
            rm $i;
            rm ${i%%_*}.py;
            rm ${i%%_*}_whole_combination.txt
        done
fi
