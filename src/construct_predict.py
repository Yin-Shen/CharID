import os
import re
import argparse
import numpy as np
from scipy.special import comb
from itertools import combinations


parser = argparse.ArgumentParser(description='''merge_pos_neg''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
args = parser.parse_args()

os.chdir(args.dirs+"/result")

def tryint(s):            
    try:
        return int(s)
    except ValueError:
        return s
def str2int(v_str):    
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]
def sort_humanly(v_list):
    return sorted(v_list, key=str2int)
chr_lst = {}
for line in open("whole_pre_experiment.bed", 'r'):
    lines = line.strip().split()
    chr_name = lines[0]
    if chr_name not in chr_lst.keys():
        chr_lst[chr_name] = []
        chr_lst[chr_name].append(lines[1:3])
    else:
        chr_lst[chr_name].append(lines[1:3])
            
len_combination_chr = {}
for key in sort_humanly(chr_lst.keys()):
        len_combination_chr[key] = int(comb(len(chr_lst[key]), 2))    
sum_combination = 0                 
for val in len_combination_chr.values():
        sum_combination += int(val) 
ocr_pool_combination_np = {}
for key in sort_humanly(chr_lst.keys()):
    if key not in ocr_pool_combination_np.keys():
        ocr_pool_combination_np[key] = []
        combination_pairs = np.array(list(combinations(list([key+'\t'+'\t'.join(vals)] for vals in chr_lst[key]), 2)))
        for i in combination_pairs:
            line = '\t'.join(''.join(l) for l in i)
            ocr_pool_combination_np[key].append(line)
for key in ocr_pool_combination_np.keys():
    o=open(key+'_whole_combination.txt', 'w')
    o.write('\n'.join(ocr_pool_combination_np[key]) + '\n')
    o.close()
