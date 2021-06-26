configfile: "config.yaml"

rule all:


rule intersect:
    input:
        bed=expand("{sample}", sample=config["bed"]),
    params:
        directory=expand("{sample}", sample=config["directory"]),
        out=config["out"]
    priority: 100
    shell:
        "mkdir $PWD/result && mkdir $PWD/log  && mkdir  $PWD/temp && cd $PWD/result && python ../src/intersect.py -d {params.directory} -b {input.bed} -o {params.out}"

rule data_preprocessing:
    input:
        genome=expand("{sample}", sample=config["genome"]),
    params:
        out=config["out"],
        outs=config["outs"]
    priority: 99
    shell:
        "cd $PWD/result && python ../src/data_preprocess.py -g {input.genome} -b {params.out}_loop_ocr.bed -o {params.outs}"

rule model_training:
    params:
        epochs=config["epochs"],
        patience=config["patience"],
        learningrate=config["learningrate"],
        batch_size=config["batch_size"],
        dropout=config["dropout"],
        nb_filter1=config["nb_filter1"],
        nb_filter2=config["nb_filter2"],
        nb_filter3=config["nb_filter3"],
        nb_filter4=config["nb_filter4"],
        filter_len1=config["filter_len1"],
        filter_len2=config["filter_len2"],
        filter_len3=config["filter_len3"],
        filter_len4=config["filter_len4"],
        pooling_size1=config["pooling_size1"],
        pooling_size2=config["pooling_size2"],
        pooling_size3=config["pooling_size3"],
        pooling_size4=config["pooling_size4"],
        GRU=config["GRU"],
        hidden=config["hidden"]
    priority: 98
    shell:
        "cd $PWD/result && python ../src/model.py -e {params.epochs} -p {params.patience} -lr {params.learningrate} -b {params.batch_size} -r {params.dropout} -n1 {params.nb_filter1} -n2 {params.nb_filter2} -n3 {params.nb_filter3} -n4 {params.nb_filter4} -fl1 {params.filter_len1} -fl2 {params.filter_len2} -fl3 {params.filter_len3} -fl4 {params.filter_len4} -ps1 {params.pooling_size1} -ps2 {params.pooling_size2} -ps3 {params.pooling_size3} -ps4 {params.pooling_size4} -gru {params.GRU} -hd {params.hidden} 2> /dev/null"

rule ap_filter:
    input:
        cooler=config["cooler"],
    params:
         resolution=config["resolution"],
         out=config["out"]
    priority: 97
    shell:
        "cd $PWD/result && python ../src/ap_filter.py -c {input.cooler} -r {params.resolution} -o {params.out} && bash ../src/cat_ap_filter.sh"

rule whole_combination:
    params:
        out=config["out"]
    priority: 96
    shell:
        "cd $PWD/result && python ../src/whole_combination.py -o {params.out}"

rule construct_negative:
    input:
        cooler=config["cooler"],
    params:
        out=config["out"]
    priority: 95
    shell:
        "cd $PWD/result &&  bash ../src/construct_negative.sh {input.cooler} {params.out}" 


rule submit_construct_negative:
    params:
        run_type=config["run_type"],
        lsf_queues=config["lsf_queues"],
        pbs_queues=config["pbs_queues"],
        jobs_number=config["jobs_number"],
        directory=config["directory"]
    priority: 94
    shell:
        "cd $PWD/result && bash ../src/submit_construct_negative.sh {params.run_type} {params.directory} {params.jobs_number} {params.lsf_queues} {params.pbs_queues} && bash ../src/cat_construct_negative.sh && bash ../src/rm_pbs_lsf.sh"

rule add_feature_pos:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 93
    shell:
        "cd $PWD/result &&  python ../src/add_feature.py -d {params.directory} -o {params.outs}"

rule add_feature_pos_signal:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 92
    shell:
        "cd $PWD/result && bash ../src/add_feature_pos.sh {params.directory} {params.outs}"

rule submit_add_feature_pos_signal:
    params:
        run_type_add_feature_pos=config["run_type_add_feature_pos"],
        lsf_queues_add_feature_pos=config["lsf_queues_add_feature_pos"],
        pbs_queues_add_feature_pos=config["pbs_queues_add_feature_pos"],
        jobs_number_add_feature_pos=config["jobs_number_add_feature_pos"],
        directory=config["directory"],
        outs=config["outs"]
    priority: 91
    shell:
        "cd $PWD/result && bash ../src/submit_add_feature_pos.sh {params.run_type_add_feature_pos} {params.directory} {params.jobs_number_add_feature_pos} {params.lsf_queues_add_feature_pos} {params.pbs_queues_add_feature_pos} && bash ../src/cat_add_feature_pos.sh {params.directory} {params.outs} && rm *.py && rm *_pos_trains.txt && bash ../src/rm_pbs_lsf.sh"

rule add_feature_neg:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 90
    shell:
        "cd $PWD/result && python ../src/add_feature_neg.py -d {params.directory} -o {params.outs}"


rule add_feature_neg_signal:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 89
    shell:
        "cd $PWD/result && bash ../src/add_feature_neg.sh {params.directory} {params.outs}"


rule submit_add_feature_neg_signal:
    params:
        run_type_add_feature_neg=config["run_type_add_feature_neg"],
        lsf_queues_add_feature_neg=config["lsf_queues_add_feature_neg"],
        pbs_queues_add_feature_neg=config["pbs_queues_add_feature_neg"],
        jobs_number_add_feature_neg=config["jobs_number_add_feature_neg"],
        directory=config["directory"],
        outs=config["outs"]
    priority: 88
    shell:
        "cd $PWD/result && bash ../src/submit_add_feature_neg.sh {params.run_type_add_feature_neg} {params.directory} {params.jobs_number_add_feature_neg} {params.lsf_queues_add_feature_neg} {params.pbs_queues_add_feature_neg} && bash ../src/cat_add_feature_neg.sh {params.directory} {params.outs} && rm *.py && rm *_neg_trains.txt && bash ../src/rm_pbs_lsf.sh"

rule merge_pos_neg:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 87
    shell:
        "cd $PWD/result && python ../src/merge_pos_neg.py -d {params.directory} -o {params.outs}"


rule train_test:
    params:
        directory=expand("{sample}", sample=config["directory"])
    priority: 86
    shell:
        "cd $PWD/result && python ../src/train_test.py -d {params.directory}"

rule submit_train_test:
    params:
        run_type_train_test=config["run_type_train_test"],
        lsf_queues_train_test=config["lsf_queues_train_test"],
        pbs_queues_train_test=config["pbs_queues_train_test"],
        jobs_number_train_test=config["jobs_number_train_test"],
        directory=config["directory"]
    priority: 85
    shell:
        "cd $PWD/result && bash ../src/submit_train_test.sh {params.run_type_train_test} {params.directory} {params.jobs_number_train_test} {params.lsf_queues_train_test} {params.pbs_queues_train_test} && bash ../src/rm_pbs_lsf.sh"
    
rule plot_cross_val:
    params:
        directory=expand("{sample}", sample=config["directory"])
    priority: 84
    shell:
        "cd $PWD/result && bash ../src/plot_cross_val.sh {params.directory} && rm *.py && rm train*.txt && rm test*.txt && rm *.model && python ../src/whole_train.py -d {params.directory}"

rule get_pos:
    input:
        genome=expand("{sample}", sample=config["genome"]),
        bed=expand("{sample}", sample=config["bed"]),
    params:
        out=config["out"],
        directory=expand("{sample}", sample=config["directory"]),
        predict_out=config["predict_out"]
    priority: 83
    shell:
        "cd $PWD/result && bedtools intersect -a {input.bed} -b {params.out}_loop_ocr.bed -v >{params.out}_nooverlap.bed && python ../src/data_preprocess_predict.py -g {input.genome} -b {params.out}_nooverlap.bed -o {params.predict_out} && python ../src/predict.py -d {params.directory} && python ../src/get_pos.py -d {params.directory} -o {params.out}"

rule construct_predict:    
    params:
        out=config["out"],
        directory=expand("{sample}", sample=config["directory"])
    priority: 82
    shell:
        "cd $PWD/result && cat whole_pos.bed {params.out}_loop_ocr.bed >whole_pre_experiment.bed && sort -Vk1 whole_pre_experiment.bed >whole_pre_experiment_sort.bed && cat {params.out}_ocr_loop.bed whole_negative.bed >whole_pos_neg.bed && sort -Vk1 whole_pos_neg.bed >whole_pos_neg_sort.bed && python ../src/construct_predict.py -d {params.directory} && bash ../src/construct_predict.sh"

rule submit_construct_predict:
    params:
        run_type_construct_predict=config["run_type_construct_predict"],
        lsf_queues_construct_predict=config["lsf_queues_construct_predict"],
        pbs_queues_construct_predict=config["pbs_queues_construct_predict"],
        jobs_number_construct_predict=config["jobs_number_construct_predict"],
        directory=config["directory"]
    priority: 81
    shell:
        "cd $PWD/result && bash ../src/submit_construct_predict.sh {params.run_type_construct_predict} {params.directory} {params.jobs_number_construct_predict} {params.lsf_queues_construct_predict} {params.pbs_queues_construct_predict} && bash ../src/cat_construct_predict.sh && bash ../src/rm_pbs_lsf.sh"

rule add_feature_predict:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 80
    shell:
        "cd $PWD/result && python ../src/add_feature_predict.py -d {params.directory} -o {params.outs}"


rule add_feature_predict_signal:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 79
    shell:
        "cd $PWD/result && bash ../src/add_feature_predict.sh {params.directory} {params.outs}"


rule submit_add_feature_predict_signal:
    params:
        run_type_add_feature_predict=config["run_type_add_feature_predict"],
        lsf_queues_add_feature_predict=config["lsf_queues_add_feature_predict"],
        pbs_queues_add_feature_predict=config["pbs_queues_add_feature_predict"],
        jobs_number_add_feature_predict=config["jobs_number_add_feature_predict"],
        directory=config["directory"],
        outs=config["outs"]
    priority: 78
    shell:
        "cd $PWD/result && bash ../src/submit_add_feature_predict.sh {params.run_type_add_feature_predict} {params.directory} {params.jobs_number_add_feature_predict} {params.lsf_queues_add_feature_predict} {params.pbs_queues_add_feature_predict} && bash ../src/cat_add_feature_predict.sh {params.directory} {params.outs} && rm *.py && rm *_predict_trains.txt && bash ../src/rm_pbs_lsf.sh"

rule batch_predict:
    params:
        directory=expand("{sample}", sample=config["directory"]),
        outs=config["outs"]
    priority: 77
    shell:
        "cd $PWD/result && head -n 1 {params.outs}_neg_train.txt >{params.outs}_neg_train_head.txt && python ../src/split.py -d {params.directory} -o {params.outs}  && bash ../src/batch_predict.sh {params.outs} {params.directory}"

rule submit_batch_predict:
    params:
        run_type_batch_predict=config["run_type_batch_predict"],
        lsf_queues_batch_predict=config["lsf_queues_batch_predict"],
        pbs_queues_batch_predict=config["pbs_queues_batch_predict"],
        jobs_number_batch_predict=config["jobs_number_batch_predict"],
        directory=config["directory"]
    priority: 76
    shell:
        "cd $PWD/result && bash ../src/submit_batch_predict.sh {params.run_type_batch_predict} {params.directory} {params.jobs_number_batch_predict} {params.lsf_queues_batch_predict} {params.pbs_queues_batch_predict} && bash ../src/batch_predict_new.sh && bash ../src/submit_batch_predict_new.sh {params.run_type_batch_predict} {params.directory} {params.jobs_number_batch_predict} {params.lsf_queues_batch_predict} {params.pbs_queues_batch_predict} && bash ../src/cat_batch_predict.sh && rm predict_ocr_loop* && rm predict_*.txt && rm whole_pre_*.txt && rm *.py && bash ../src/rm_pbs_lsf.sh"

rule cluster:
    params:
        run_type_cluster=config["run_type_cluster"],
        lsf_queues_cluster=config["lsf_queues_cluster"],
        pbs_queues_cluster=config["pbs_queues_cluster"],
        jobs_number_cluster=config["jobs_number_cluster"],
        directory=config["directory"]
    priority: 75
    shell:
        "cd $PWD/result && python ../src/cluster_split_chrom.py -d {params.directory} && bash ../src/cluster.sh && bash ../src/submit_cluster.sh {params.run_type_cluster} {params.directory} {params.jobs_number_cluster} {params.lsf_queues_cluster} {params.pbs_queues_cluster} && bash ../src/cat_cluster.sh && rm chr*_predict.py && bash ../src/cluster_bedpe.sh && bash ../src/rm_pbs_lsf.sh"

rule rename:
    params:
        out=config["out"]
    priority: 74
    shell:
        "cd $PWD/result && mv result_whole.svg CharID_Loop_Model_ROC.svg && mv pictureROC.png CharID_Anchor_Model_ROC.png && mv pictureloss.png CharID_Anchor_Model_Loss.png && mv picturehistory.png CharID_Anchor_Model_History.png && mv whole_pos.bed CharID_Anchor_Model_predict.bed && mv gbdt.model CharID_Loop_Model.model && mv model_architecture.json CharID_Anchor_Model_architecture.json && mv model_weights.h5 CharID_Anchor_Model_weights.h5 && mv predict_cluster.bedpe CharID_Loop_Model_predict.bedpe && ls | egrep -v 'CharID_Loop_Model_ROC.svg|CharID_Anchor_Model_ROC.png|CharID_Anchor_Model_Loss.png|CharID_Anchor_Model_History.png|CharID_Anchor_Model_predict.bed|CharID_Loop_Model.model|CharID_Anchor_Model_architecture.json|CharID_Anchor_Model_weights.h5|CharID_Loop_Model_predict.bed' | xargs -I file mv file ../temp"
