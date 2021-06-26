for file in ${1}/result/*.py
do
        fq=$(basename $file | sed 's/.py//')
        echo "
        #PBS -N add_feature_neg_$fq
        #PBS -l nodes=1:ppn=1
        #PBS -l walltime=1200:00:00
        #PBS -o ../log/add_feature_neg_$fq.out
        #PBS -e ../log/add_feature_neg_$fq.err
        #PBS -q ${2}
        #PBS -V
        #PBS -S /bin/bash
        python ${1}/result/$file
        " >run$fq.pbs
        qsub run$fq.pbs
done

