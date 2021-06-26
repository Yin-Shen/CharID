#! /bin/bash
cd ../result
MAXINDEX=`find . -name "chr*_predict.py" |wc -l`
File=`ls cluster_chr*.bed 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
    File=`ls cluster_chr*.bed 2>/dev/null |wc -w`
    sleep 200
done
if [ $File = ${MAXINDEX} ]
    then
        for i in `ls cluster_chr*.bed|sort -V`
        do
            echo "File name is: $i";
            cat $i >> predict_cluster.bed;
            rm $i;
        done
fi
