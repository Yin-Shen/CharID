import argparse
import os

parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()

os.chdir(args.dirs+"/result")
genome=[]
genome_line=0
for l in open(args.out+"_nooverlap.bed",'r'):
    ll=l.strip()
    genome.append(ll)
    genome_line +=1 

predict=[]
for line in open('predict_whole.txt','r'):
    lines=line.strip()
    liness=lines.lstrip('[').rstrip(']')
    predict.append(liness)


genome_pre={}
lines=0
while lines < genome_line:
    k_name=genome[lines]
    genome_pre[k_name]=predict[lines]
    lines+=1

o=open('whole_pos.bed','w')
for k,v in genome_pre.items():
    if genome_pre[k] == '1':
        o.write(k+'\n')
o.close()


