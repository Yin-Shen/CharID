for file in ${1}/result/*.py
do
        fq=$(basename $file | sed 's/.py//')
        echo "
        #PBS -N train_test_$fq
        #PBS -l nodes=1:ppn=1
        #PBS -l walltime=1200:00:00
        #PBS -o ../log/train_test_$fq.out
        #PBS -e ../log/train_test_$fq.err
        #PBS -q ${2}
        #PBS -V
        #PBS -S /bin/bash
        python ${1}/result/$file
        " >run$fq.pbs
        qsub run$fq.pbs
done

