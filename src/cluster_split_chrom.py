import argparse
import pandas as pd
import os
parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
args = parser.parse_args()

os.chdir(args.dirs+"/result") 
chrom = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10','11', '12', '13', '14', '15', '16', '17', '18', '19','20','21','22','X']
loops = pd.read_table("predict.bed", header=None)
for i in chrom:                                                                         
   loop = loops.loc[loops[0]=='chr'+str(i)]
   loop.to_csv('chr'+str(i)+'_predict.bed',sep='\t', index=False, header = None) 
