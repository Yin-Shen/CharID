import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()

os.chdir(args.dirs+"/result")

train = pd.read_table(args.out+"_predict_train.txt")
size = 200000
list_of_dfs = [train.loc[i:i+size-1,:] for i in range(0, len(train),size)]
for i,df in enumerate(list_of_dfs):
    df.to_csv('predict_ocr_loop'+str(i),sep='\t', index=False)

