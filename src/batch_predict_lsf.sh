for file in ${1}/result/predict_ocr_loop*.py
do
        fq=$(basename $file | sed 's/.py//')
        echo "
        #BSUB -J batch_predict_$fq
        #BSUB -n 1
        #BSUB -R span[hosts=1]
        #BSUB -q ${2}
        #BSUB -o ../log/%J.out
        #BSUB -e ../log/%J.err
        python $file
        " >run$fq.lsf
        bsub <run$fq.lsf
done

