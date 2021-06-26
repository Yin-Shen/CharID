for file in ${1}/result/whole_predict_*.py
do
        fq=$(basename $file | sed 's/.py//')
        echo "
        #PBS -N batch_predict_new_$fq
        #PBS -l nodes=1:ppn=1
        #PBS -l walltime=1200:00:00
        #PBS -o ../log/batch_predict_new_$fq.out
        #PBS -e ../log/batch_predict_new_$fq.err
        #PBS -q ${2}
        #PBS -V
        #PBS -S /bin/bash
        python ${1}/result/$file
        " >run$fq.pbs
        qsub run$fq.pbs
done

