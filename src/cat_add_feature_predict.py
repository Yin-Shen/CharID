import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()

os.chdir(args.dirs+"/result")
file_path = os.getcwd()
files = os.listdir(file_path)
len_outs = len(args.out)
signal_files = []
for file in files:
    if file[-19::] == '_predict_trains.txt':
        signal_files.append(file[int(len_outs)+1:-19])
train = pd.read_table(args.dirs+"/result/"+args.out+"_predict_train.txt")
for signal in signal_files:
    train_new = pd.read_table(args.out+"_"+str(signal)+"_predict_trains.txt")
    signal3 = str(signal)+'in_between'
    signal4 = 'avg_'+str(signal)
    signal5 = 'std_'+str(signal)
    train[signal3] = train_new[signal3]
    train[signal4] = train_new[signal4]
    train[signal5] = train_new[signal5]
cols = list(train)
cols.insert(0,cols.pop(cols.index('chrom1')))
cols.insert(1,cols.pop(cols.index('start1')))
cols.insert(2,cols.pop(cols.index('end1')))
cols.insert(3,cols.pop(cols.index('chrom2')))
cols.insert(4,cols.pop(cols.index('start2')))
cols.insert(5,cols.pop(cols.index('end2')))
train = train.loc[:,cols]
train.drop('index',axis=1, inplace=True)
train.to_csv(args.out+'_predict_train.txt',sep='\t', index=False)

