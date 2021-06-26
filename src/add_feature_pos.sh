cd ${1}"/signal"
for i in *.bigWig
do
cat>${1}"/result/${i%%.bigWig}.py"<<EOF
import pandas as pd
import numpy as np
import HTSeq
import os
import pyBigWig

train = pd.read_table("${1}/result/whole_ocr_loop_ap_filter_new.bed")
avg_signal = []
std_signal = []
signal_in_between = []
for index,row in train.iterrows():
    bw_signal = pyBigWig.open("${1}/signal/$i")
    chrom1 = row['chrom1']
    start1 = row['start1']
    end1 = row['end1']
    chrom2 = row['chrom2']
    start2 = row['start2']
    end2 = row['end2']
    if bw_signal.stats(chrom1, int(start1)-2000, int(end1)+2000) == [None]:
        signal_1 = 0
    else:
        signal_1 = float(''.join(str(v) for v in bw_signal.stats(chrom1, int(start1)-2000, int(end1)+2000)))
    if bw_signal.stats(chrom2, int(start2)-2000, int(end2)+2000) == [None]:
        signal_2 = 0
    else:
        signal_2 = float(''.join(str(v) for v in bw_signal.stats(chrom1, int(start2)-2000, int(end2)+2000)))
    avg_signal.append((signal_1 + signal_2)/2.0)
    std_signal.append(np.std([signal_1, signal_2]))
    if int(end1) < int(start2):
        if bw_signal.stats(chrom1, int(end1), int(start2)) == [None]:
            signal_3 = 0
        else:
            signal_3 = float(''.join(str(v) for v in bw_signal.stats(chrom1, int(end1), int(start2))))
    else:
        if bw_signal.stats(chrom1, int(start2), int(end1)) == [None]:
            signal_3 = 0
        else:
            signal_3 = float(''.join(str(v) for v in bw_signal.stats(chrom1, int(start2), int(end1))))    
    signal_in_between.append(signal_3)
signal1 = 'avg_${i%%.bigWig}'
signal2 = 'std_${i%%.bigWig}'
signal3 = '${i%%.bigWig}in_between'         
train[signal1] = pd.Series(avg_signal, index = train.index)
train[signal2] = pd.Series(std_signal, index = train.index)
train[signal3] = pd.Series(signal_in_between, index = train.index)
train.to_csv("${2}_${i%%.bigWig}_pos_trains.txt",sep='\t', index=False)
EOF
done
