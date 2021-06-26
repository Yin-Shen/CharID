for file in ${1}/result/*.py
do
        fq=$(basename $file | sed 's/.py//')
        echo "
        #BSUB -J add_feature_neg_$fq
        #BSUB -n 1
        #BSUB -R span[hosts=1]
        #BSUB -q ${2}
        #BSUB -o ../log/%J.out
        #BSUB -e ../log/%J.err
        python $file
        " >run$fq.lsf
        bsub <run$fq.lsf
done

