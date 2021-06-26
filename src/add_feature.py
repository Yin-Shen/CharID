import pandas as pd
import numpy as np
import HTSeq
import argparse
import GenomeData



parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()


def assign_motif_pattern(strand1, strand2):
    if (strand1 == '-' and strand2 == '+'):
        return '2'
    elif (strand1 == '+' and strand2 == '-'):
        return '4'
    else:
        return '3'


def find_motif_pattern(anchor1, anchor2, motif):
    """
     Input:
         anchor = HTSeq.GenomicInterval(chrom,summit-ext, summit+ext,'.')
         motif = {'chromXX':{start:(strand, score)}}
     Output:
         a tuple (pattern, avg_motif_strength, std_motif_strength)
     Rules to assign motif pattern:
     1. Both anchors have no motif, assign 0;
     2. One anchor has no motif, no matter how many motifs the other anchor may have, assign 1;
     3. Both anchors have 1 motif: no ambuguity, divergent=2;tandem=3; convergent=4
     4. Anchors have multiple motifs: in each anchor, choose the one with the highest motif strength
    """
    chrom = anchor1.chrom
    starts = list(motif[chrom].keys())
    num1 = 0
    starts1 = []
    scores1 = []
    for start in starts:
        if start >= anchor1.start and start <= anchor1.end:
            num1 += 1
            starts1.append(start)
            scores1.append(motif[chrom][start][1])
    num2 = 0
    starts2 = []
    scores2 = []
    for start in starts:
        if start >= anchor2.start and start <= anchor2.end:
            num2 += 1
            starts2.append(start)
            scores2.append(motif[chrom][start][1])

    if num1 ==0 and num2 == 0:
        return (0,0,0)
    else:
        if (num1*num2 == 0):
            if num1 == 0:
                return (1, max(scores2)/2.0, np.std([0, max(scores2)]))
            else:
                return (1, max(scores1)/2.0, np.std([0, max(scores1)]))
        else:
            if (num1 == 1 and num2 == 1):
                strand1 = motif[chrom][starts1[0]][0]
                strand2 = motif[chrom][starts2[0]][0]
                pattern = assign_motif_pattern(strand1, strand2)
                return (pattern, np.mean([max(scores1),max(scores2)]), np.std([max(scores1),max(scores2)]))
            else:
                index1 = scores1.index(max(scores1))
                strand1 = motif[chrom][starts1[index1]][0]
                index2 = scores2.index(max(scores2))
                strand2 = motif[chrom][starts2[index2]][0]
                pattern = assign_motif_pattern(strand1, strand2)
                return (pattern, np.mean([max(scores1),max(scores2)]), np.std([max(scores1),max(scores2)]))    

train = pd.read_table(args.dirs+"/result/whole_ocr_loop_ap_filter.bed", header=None)
train.loc[-1]=['chrom1','start1','end1','chrom2','start2','end2']
train.index = train.index + 1
train = train.sort_index()
train.to_csv(args.dirs+"/result/whole_ocr_loop_ap_filter_new.bed",sep='\t',header=None, index=False)

train = pd.read_table(args.dirs+"/result/whole_ocr_loop_ap_filter_new.bed")
train = train.sort_values(by=['chrom1','start1','start2'], axis = 0, ascending=[1,1,1])


anchors = {}
for index,row in train.iterrows():
    chrom = row['chrom1']
    if chrom not in anchors.keys():
        anchors[chrom] = set()
    anchors[chrom].add(row['start1'])
    anchors[chrom].add(row['start2'])
for chrom in anchors.keys():
    anchors[chrom] = list(anchors[chrom])
    anchors[chrom].sort()


info = pd.read_table(args.dirs+"/signal/CTCF_motifs_p1e-5_with_phastCons.txt")


motif = {}  # motif = {'chromXX':{start:(strand, score)}}
for index, row in info.iterrows():
    chrom = row['chrom']
    start = row['start']
    strand = row['strand']
    score = row['score']


    if chrom not in motif.keys():
        motif[chrom] = {}
    motif[chrom][start] = (strand, score)


motif_pattern = []
avg_motif_strength_list = []
std_motif_strength_list = []    


for index, row in train.iterrows():
    chrom1 = row['chrom1']
    start1 = row['start1']
    end1 = row['end1']
    anchor1 = HTSeq.GenomicInterval(chrom1, start1, end1, '.')
    chrom2 = row['chrom2']
    start2 = row['start2']
    end2 = row['end2']
    anchor2 = HTSeq.GenomicInterval(chrom2, start2, end2, '.')
    (pattern, avg_motif_strength, std_motif_strength) = find_motif_pattern(anchor1, anchor2, motif)
    motif_pattern.append(pattern)
    avg_motif_strength_list.append(avg_motif_strength)
    std_motif_strength_list.append(std_motif_strength)


train['motif_pattern'] = pd.Series(motif_pattern, index = train.index)
train['avg_motif_strength'] = pd.Series(avg_motif_strength_list, index = train.index)
train['std_motif_strength'] = pd.Series(std_motif_strength_list, index = train.index)
train['length'] = abs(train['start2'] - train['end1'])


starts = {}
cvg = {}
training = []
ext = 20
chroms = GenomeData.hg19_chroms                                                                                 
for chrom in chroms:                                    
    chrom_train = train[train['chrom1'] == chrom].copy()
    chrom_train.reset_index(inplace=True)         
    cvg = [0]*GenomeData.hg19_chrom_lengths[chrom]               
    phastCon = args.dirs+"/signal/phastCon_raw"+"/"+chrom+".phastCons100way.wigFix"
    wiggle = open(phastCon,'r')
    for line in wiggle:   
        if line[0] == 'f':                                   
            i = 0                                                                        
            start = int(line.strip().split(' ')[2].split('=')[1])
        else:                                  
            signal = line.strip().split(' ')[0]       
            if signal == 'NA':                        
                signal = 0
            else:                     
                signal = float(signal)
            cvg[start + i] = signal
            i += 1
    wiggle.close()
    AvgCons = []
    DevCons = []
    for index, row in chrom_train.iterrows():
        con1 = sum(cvg[(row['start1']-ext): (row['start1']+ext)])
        con2 = sum(cvg[(row['start2']-ext): (row['start2']+ext)])
        AvgCons.append((con1+con2)/2.0)
        DevCons.append(np.std([con1, con2]))
    chrom_train['avg_conservation'] = pd.Series(AvgCons)
    chrom_train['std_conservation'] = pd.Series(DevCons)
    training.append(chrom_train)
train = pd.concat(training, ignore_index=True)
train['response'] = 1
train.to_csv(args.out+'_pos_train.txt',sep='\t', index=False)
