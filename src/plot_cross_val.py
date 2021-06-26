import os
import numpy as np
import pandas as pd
import argparse
from scipy import interp
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve, auc
from sklearn.externals import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='''merge_pos_neg''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
args = parser.parse_args()


mean_fpr=np.linspace(0,1,100)
tprs = []
aucs = []
i = 0
y_real = []
y_proba = []
f, axes = plt.subplots(1, 2, figsize=(10, 5))

os.chdir(args.dirs+"/result")
file_path = os.getcwd()
files = os.listdir(file_path)
model_files = []
for file in files:
    if file[-6:] == '.model':
        model_files.append(file)
for file in model_files:
    gbdt = joblib.load(file)
    test = pd.read_table('test'+str(file[4:-6])+'.txt')
    data_test = test.iloc[:,7:].as_matrix()
    label_test = np.array(test['response'])
    y_pred_pro = gbdt.predict_proba(data_test)[:,1]
    y_scores = y_pred_pro
    fpr, tpr, thresholds_gbdt = roc_curve(label_test, y_scores)
    tprs.append(interp(mean_fpr,fpr,tpr))
    tprs[-1][0]=0.0
    roc_auc=auc(fpr,tpr)
    aucs.append(roc_auc)
    precision, recall, _ = precision_recall_curve(label_test, y_scores)
    axes[1].step(recall, precision, lw=1, alpha=0.3)
    y_real.append(label_test)
    y_proba.append(y_scores)
    axes[0].plot(fpr,tpr,lw=1,alpha=0.3)
    i +=1

mean_tpr=np.mean(tprs,axis=0)
mean_tpr[-1]=1.0
mean_auc=auc(mean_fpr,mean_tpr)
std_auc=np.std(tprs,axis=0)
axes[0].plot(mean_fpr,mean_tpr,color='black',label=r'Mean ROC (area=%0.3f)'%mean_auc,lw=2,alpha=.8)
std_tpr=np.std(tprs,axis=0)
tprs_upper=np.minimum(mean_tpr+std_tpr,1)
tprs_lower=np.maximum(mean_tpr-std_tpr,0)
axes[0].fill_between(mean_tpr,tprs_lower,tprs_upper,color='gray',alpha=.2)
axes[0].set_xlim([-0.05,1.05])
axes[0].set_ylim([-0.05,1.05])
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].legend(loc='lower right')

y_real = np.concatenate(y_real)
y_proba = np.concatenate(y_proba)
precision, recall, _ = precision_recall_curve(y_real, y_proba)
lab = 'Mean PR (area=%0.3f)' % (auc(recall, precision))
axes[1].step(recall, precision, label=lab, lw=2, color='black')
axes[1].set_xlabel('Recall')
axes[1].set_ylabel('Precision')
axes[1].legend(loc='lower left', fontsize='small')
f.tight_layout()
f.savefig('result_whole.svg')

