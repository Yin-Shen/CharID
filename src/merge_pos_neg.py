import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='''merge_pos_neg''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()


train_pos = pd.read_table(args.dirs+"/result/"+args.out+"_pos_train.txt")
train_neg = pd.read_table(args.dirs+"/result/"+args.out+"_neg_train.txt")
train_whole = pd.concat([train_pos, train_neg])
train_whole = train_whole.sort_values(by=['chrom1','start1','start2'], axis = 0, ascending=[1,1,1])
cols = list(train_whole)
cols.insert(0,cols.pop(cols.index('chrom1')))
cols.insert(1,cols.pop(cols.index('start1')))
cols.insert(2,cols.pop(cols.index('end1')))
cols.insert(3,cols.pop(cols.index('chrom2')))
cols.insert(4,cols.pop(cols.index('start2')))
cols.insert(5,cols.pop(cols.index('end2')))
cols.insert(6,cols.pop(cols.index('response')))
train_whole = train_whole.loc[:,cols]
train_whole.to_csv(args.dirs+"/result/"+"whole_train.txt", sep='\t', index=False)
