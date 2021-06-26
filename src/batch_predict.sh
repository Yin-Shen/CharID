for i in predict_ocr_loop*
do
cat>$i.py<<EOF
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

test = pd.read_table('$i')
header = pd.read_table('${1}_neg_train_head.txt')
header.drop('response',axis=1, inplace=True)
cols = list(test)
for i, j in enumerate(header.columns):
    cols.insert(i ,cols.pop(cols.index(j)))
test_whole = test.loc[:,cols]
data_test = test_whole.iloc[:,6:].as_matrix()
data_test = np.nan_to_num(data_test)

gbdt = joblib.load('${2}/result/gbdt.model')
pred = gbdt.predict_proba(data_test)
o=open('predict_${i#*predict_ocr_loop}.txt','w')

for i in pred.tolist():
    if float(list(i)[1]) > 0.5:
       o.write(str('1')+'\t'+str(list(i)[1])+'\n')
    else:
       o.write(str('0')+'\t'+str(list(i)[1])+'\n')
o.close()
EOF
done

