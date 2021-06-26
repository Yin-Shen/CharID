for file in ${1}/result/whole_predict_*.py
do
        fq=$(basename $file | sed 's/.py//')
        echo "
        #BSUB -J batch_predict_new_$fq
        #BSUB -n 1
        #BSUB -R span[hosts=1]
        #BSUB -q ${2}
        #BSUB -o ../log/%J.out
        #BSUB -e ../log/%J.err
        python $file
        " >run$fq.lsf
        bsub <run$fq.lsf
done

