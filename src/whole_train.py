import os
import argparse
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
import numpy as np
import pandas as pd


parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
args = parser.parse_args()


os.chdir(args.dirs+"/result")

train = pd.read_table("whole_train.txt")
cols = list(train)
cols.insert(0,cols.pop(cols.index('chrom1')))
cols.insert(1,cols.pop(cols.index('start1')))
cols.insert(2,cols.pop(cols.index('end1')))
cols.insert(3,cols.pop(cols.index('chrom2')))
cols.insert(4,cols.pop(cols.index('start2')))
cols.insert(5,cols.pop(cols.index('end2')))
cols.insert(6,cols.pop(cols.index('response')))
train = train.loc[:,cols]

X_train = train.iloc[:,7:].as_matrix()
Y_train = np.array(train['response'])


gbm0 = GradientBoostingClassifier(n_estimators=235, random_state=10)
gbm0.fit(X_train,Y_train)
joblib.dump(gbm0, 'gbdt.model')

