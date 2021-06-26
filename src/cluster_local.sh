#!/bin/bash
cd ${1}/result
MAXINDEX=`ls chr*_predict.py |wc -l`
[ -e /tmp/fd1 ] || mkfifo /tmp/fd1
exec 3<>/tmp/fd1
rm -rf /tmp/fd1
for ((i=1; i<=${2}; i++))
do
        echo >&3
done
for i in chr*_predict.py
do
read -u3 
{
        python $i 2> /dev/null
        sleep 1
        echo 'success_'${i}       
        echo >&3
}&
done
wait


exec 3<&-
exec 3>&-

