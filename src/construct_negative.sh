for i in chr*_ocr_loop_whole_combination.txt
do
cat>${i%%_*}.py<<EOF
import cooler
import numpy as np
import pandas as pd
def my_count(row):
    start1 = int(((int(row[2]) - int(row[1])) / 2) + int(row[1]))
    start2 = int(((int(row[5]) - int(row[4])) / 2) + int(row[4]))
    score = chr_matrix[int(start1/5000), int(start2/5000)]
    score_square = chr_matrix[int(start1/5000)-1:int(start1/5000)+2, int(start2/5000)-1:int(start2/5000)+2]
    if np.isnan(score_square).sum() == 9:
        return 0
    else:
        score_square_mean = score_square[~np.isnan(score_square)].mean()
        if int(score_square_mean) == 0:
           return 0
        else:
           AP_score = score / score_square_mean
           return AP_score

c = cooler.Cooler("${1}")
chr_matrix = c.matrix(sparse=False).fetch('${i%%_*}')
whole_ocr_loop_pool1 = pd.read_table('${2}_ocr_loop.bed', header=None)
whole_ocr_loop_pool =  pd.read_table('whole_ocr_loop_ap_filter.bed', header=None)
whole_ocr_loop_pool['df'] = whole_ocr_loop_pool[4] - whole_ocr_loop_pool[2]
ocr_pool_combination_np = pd.read_table('$i', header=None)
negtivate_loops_pool = ocr_pool_combination_np[~ocr_pool_combination_np.isin(whole_ocr_loop_pool1)].dropna()
negtivate_loops_pool['df'] = negtivate_loops_pool[4] - negtivate_loops_pool[2]
negtivate_loops_pool[1] = negtivate_loops_pool[1].astype('int')
negtivate_loops_pool[2] = negtivate_loops_pool[2].astype('int')
negtivate_loops_pool[4] = negtivate_loops_pool[4].astype('int')
negtivate_loops_pool[5] = negtivate_loops_pool[5].astype('int')
negtivate_loops_pool['df'] = negtivate_loops_pool['df'].astype('int')
negtivate_loops_pool_new = negtivate_loops_pool.loc[(negtivate_loops_pool['df'].abs() >= 10000) & (negtivate_loops_pool['df'].abs() <= 2000000)]
negtivate_loops_pool_new['AP'] = negtivate_loops_pool_new.apply(lambda row: my_count(row), axis=1)
negtivate_loops_pool_news = negtivate_loops_pool_new.loc[negtivate_loops_pool_new['AP'] < 1]
d_ocr_loop = whole_ocr_loop_pool.loc[whole_ocr_loop_pool[0] == '${i%%_*}']['df'].values
s_ocr_loop = pd.Series(d_ocr_loop)
bins = list(i for i in range(0, 2000001, 10000))
labels = []                                                                            
for i in range(len(bins)):                                                             
    if i + 1 < len(bins):                                                              
        labels.append('{}-{}'.format(bins[i], bins[i+1]))                              
    else:
        break
groups_ocr_loop = pd.cut(s_ocr_loop, bins=bins, labels = labels)
num_range = int(whole_ocr_loop_pool.loc[whole_ocr_loop_pool[0]=='${i%%_*}'].shape[0])
for i, v in groups_ocr_loop.value_counts().items():
    negtivate_loops_pool_newss = negtivate_loops_pool_news.loc[(negtivate_loops_pool_news['df'].abs() >= int(i.split('-')[0])) &  (negtivate_loops_pool_news['df'].abs() <= int(i.split('-')[1]))]
    if 'negtivate_loops_pool_final' not in dir():
        if int(negtivate_loops_pool_newss.shape[0]) <= v:
            negtivate_loops_pool_final = negtivate_loops_pool_newss
        else:
            negtivate_loops_pool_final = negtivate_loops_pool_newss.sample(n=v, frac=None, replace=False, weights=None, random_state=None, axis=None)
    else:
        if int(negtivate_loops_pool_newss.shape[0]) <= v:
            negtivate_loops_pool_final1 = negtivate_loops_pool_newss
            negtivate_loops_pool_final = pd.concat([negtivate_loops_pool_final, negtivate_loops_pool_final1])
        else:
            negtivate_loops_pool_final1 = negtivate_loops_pool_newss.sample(n=v, frac=None, replace=False, weights=None, random_state=None, axis=None)
            negtivate_loops_pool_final = pd.concat([negtivate_loops_pool_final, negtivate_loops_pool_final1])
negtivate_loops_pool_finals = negtivate_loops_pool_final.drop(['df'],axis=1)
negtivate_loops_pool_finals = negtivate_loops_pool_finals.drop(['AP'],axis=1)
negtivate_loops_pool_finals.to_csv('${i%%_*}_neg.txt',sep='\t', index=False, header = None)
EOF
done
