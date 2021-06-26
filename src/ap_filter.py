import cooler
import numpy as np
import argparse
import pandas as pd

#Argument parsing
parser = argparse.ArgumentParser(description='''ap filter''')
parser.add_argument("--cooler", "-c", required=True,
                    help="cooler file")
parser.add_argument("--resolution", "-r", default=5000, type=int, required=True,
                    help="resolution")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()


def my_count(row):
    start1 = int(((int(row[2]) - int(row[1])) / 2) + int(row[1]))
    start2 = int(((int(row[5]) - int(row[4])) / 2) + int(row[4]))
    score = chr_matrix[int(start1/int(args.resolution)), int(start2/int(args.resolution))]
    score_square = chr_matrix[int(start1/int(args.resolution))-1:int(start1/int(args.resolution))+2, int(start2/int(args.resolution))-1:int(start2/int(args.resolution))+2]
    if np.isnan(score_square).sum() == 9:
        return 0
    else:
        score_square_mean = score_square[~np.isnan(score_square)].mean()
        if int(score_square_mean) == 0:
           return 0
        else:
           AP_score = score / score_square_mean
           return AP_score

c = cooler.Cooler(args.cooler)
whole_ocr_loop_pool =  pd.read_table(args.out+'_ocr_loop.bed', header=None)

chr_name_list = list(['chr'+str(i) for i in range(1, 23)] + ['chrX'])
for chr_name in chr_name_list:
    chr_matrix = c.matrix(sparse=False).fetch(chr_name)
    whole_ocr_loop_pool_new = whole_ocr_loop_pool.loc[whole_ocr_loop_pool[0] == chr_name]
    whole_ocr_loop_pool_new['AP'] = whole_ocr_loop_pool_new.apply(lambda row: my_count(row),axis=1)
    whole_ocr_loop_pool_news = whole_ocr_loop_pool_new.loc[whole_ocr_loop_pool_new['AP'] >= 1.2]
    whole_ocr_loop_pool_newss = whole_ocr_loop_pool_news.drop(['AP'],axis=1)
    whole_ocr_loop_pool_newss.to_csv(str(chr_name)+'_ap_filter.txt',sep='\t', index=False, header = None)

