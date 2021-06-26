cd ../result
MAXINDEX=`ls whole_predict_*.py |wc -l`
File=`ls whole_pre_*.txt 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
    File=`ls whole_pre_*.txt 2>/dev/null |wc -w`
    sleep 200
done
if [ $File = ${MAXINDEX} ]
    then
        for i in `ls whole_pre_*.txt |sort -V`
        do
        echo "File name is: $i";
        cat $i >> predict.bed;
        done
fi

