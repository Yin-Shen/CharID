import os
import argparse
import itertools

parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
args = parser.parse_args()


os.chdir(args.dirs+"/result")
chr_name_list = list(['chr'+str(i) for i in range(1, 23)] + ['chrX'])
combinations = list(itertools.combinations(chr_name_list, 2))

python_file1 = '''
import re,os,sys
from optparse import OptionParser
import sklearn
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from scipy import interp
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from scipy import interp
import matplotlib.pyplot as plt

data = pd.read_table("whole_train.txt")

'''

python_file2 = '''
train = data.drop(test.index)
cols = list(train)
cols.insert(0,cols.pop(cols.index('chrom1')))
cols.insert(1,cols.pop(cols.index('start1')))
cols.insert(2,cols.pop(cols.index('end1')))
cols.insert(3,cols.pop(cols.index('chrom2')))
cols.insert(4,cols.pop(cols.index('start2')))
cols.insert(5,cols.pop(cols.index('end2')))
cols.insert(6,cols.pop(cols.index('response')))
train = train.loc[:,cols]


cols = list(test)
cols.insert(0,cols.pop(cols.index('chrom1')))
cols.insert(1,cols.pop(cols.index('start1')))
cols.insert(2,cols.pop(cols.index('end1')))
cols.insert(3,cols.pop(cols.index('chrom2')))
cols.insert(4,cols.pop(cols.index('start2')))
cols.insert(5,cols.pop(cols.index('end2')))
cols.insert(6,cols.pop(cols.index('response')))
test = test.loc[:,cols]
'''
python_file3 = '''
X_train = train.iloc[:,7:].as_matrix()
X_train = np.nan_to_num(X_train)
Y_train = np.array(train['response'])
X_test = test.iloc[:,7:].as_matrix()
X_test = np.nan_to_num(X_test)
Y_test = np.array(test['response'])

gbm0 = GradientBoostingClassifier(n_estimators = 8000, learning_rate = 0.1, max_depth = 5, max_features = 'log2', random_state = 10)
gbm0.fit(X_train,Y_train)
y_pred_pro = gbm0.predict_proba(X_test)[:,1]
fpr_gbdt, tpr_gbdt, thresholds_gbdt = roc_curve(Y_test, y_pred_pro)
roc_auc_gbdt = auc(fpr_gbdt, tpr_gbdt)
precision_gbdt, recall_gbdt, thresholds_gbdt = precision_recall_curve(Y_test,y_pred_pro)
pr_auc_gbdt= auc(recall_gbdt,precision_gbdt)
print("roc_auc is %s" % (roc_auc_gbdt))
print("pr_auc is %s" % (pr_auc_gbdt))
'''

for i, comb in enumerate(combinations):
    file_read = open('chr'+str(i)+'.py', 'w') 
    file_read.write(python_file1+'\n'+"test = data.query('chrom1==\""+comb[0]+"\" | chrom1==\""+comb[1]+"\"')"+ '\n'+ python_file2 + '\n'+ "train.to_csv('train"+str(i)+".txt',sep='\\t', index=False)"+'\n'+"test.to_csv('test"+str(i)+".txt',sep='\\t', index=False)"+'\n'+python_file3+'\n'+"joblib.dump(gbm0, 'gbdt"+str(i)+".model')"+ '\n')
    file_read.close()
