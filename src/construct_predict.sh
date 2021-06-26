for i in chr*_whole_combination.txt
do
cat>${i%%_*}.py<<EOF
import pandas as pd
whole_ocr_loop_pool =  pd.read_table("whole_pos_neg_sort.bed", header=None)
ocr_pool_combination_np = pd.read_table('$i', header=None)
negtivate_loops_pool = ocr_pool_combination_np[~ocr_pool_combination_np.isin(whole_ocr_loop_pool)].dropna()
negtivate_loops_pool['df'] = negtivate_loops_pool[4] - negtivate_loops_pool[2]
negtivate_loops_pool[1] = negtivate_loops_pool[1].astype('int')
negtivate_loops_pool[2] = negtivate_loops_pool[2].astype('int')
negtivate_loops_pool[4] = negtivate_loops_pool[4].astype('int')
negtivate_loops_pool[5] = negtivate_loops_pool[5].astype('int')
negtivate_loops_pool['df'] = negtivate_loops_pool['df'].astype('int')
negtivate_loops_pool_new = negtivate_loops_pool.loc[(negtivate_loops_pool['df'].abs() >= 10000) & (negtivate_loops_pool['df'].abs() <= 2000000)]
negtivate_loops_pool_news = negtivate_loops_pool_new.drop(['df'],axis=1)
negtivate_loops_pool_news.to_csv('${i%%_*}_predict.txt',sep='\t', index=False, header = None)
EOF
done
