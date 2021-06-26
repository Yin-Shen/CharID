#!/bin/bash
cd ${1}/result
MAXINDEX=`find . -name "chr*.py" |wc -l`
[ -e /tmp/fd1 ] || mkfifo /tmp/fd1
exec 3<>/tmp/fd1
rm -rf /tmp/fd1
for ((i=1; i<=${2}; i++))
do
        echo >&3
done
for ((i=1; i<=${MAXINDEX}; i++))
do
read -u3 
{
        python chr$i.py 2> /dev/null
        sleep 1
        echo 'success_'${i}       
        echo >&3
}&
done
wait


exec 3<&-
exec 3>&-

