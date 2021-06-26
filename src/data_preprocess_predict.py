'''
This script is preprocess data for charid-anchor model

Author: Yin Shen
'''

#Required Modules
import numpy as np
import re
import random
import argparse




#Argument parsing
parser = argparse.ArgumentParser(description='''Data Preprocess: 
                                                takes 3 required arguments''')
parser.add_argument("--genome", "-g", required=True,
                    help="genome file in fasta format")
parser.add_argument("--bed", "-b", required=True,
                    help="bed file of Chromatin Accessible Regions for input")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()

#Construct a positive sample sequences
genome_fasta={}
for line in open(args.genome,'r'):
    if line[0]=='>':
        seq_name=line.lstrip('>').strip()
        genome_fasta[seq_name]=[]
    else:
        genome_fasta[seq_name].append(line.strip())
for keys,val in genome_fasta.items():
    genome_fasta[keys]=''.join(val)
nuc=open(args.bed,'r')
out=open(args.out+".fa",'w')
col_num=0
bed=nuc.readlines()
col=len(bed)
for lline in bed:
        col_num+=1
        chr_name=lline.rstrip().split()[0]
        start_end=lline.rstrip().split()[1:]
        leng=int(start_end[1])-int(start_end[0])
        out.write('>'+chr_name+':'+start_end[0]+'-'+start_end[1]+'\n'+genome_fasta[chr_name][int(start_end[0]):int(start_end[1])]+'\n')
out.close()

#Construct a positive samples datasets
bed_dict_pos={}
pos_o=open(args.out+"pos.txt",'w')
for line in open(args.out+".fa",'r'):
    if line[0]==">":
       seq=line.strip()
       bed_dict_pos[seq]=[]
    else:
       bed_dict_pos[seq].append(line.strip())
for keys,val in bed_dict_pos.items():
    bed_dict_pos[keys]=''.join(val)
    pos_o.write('1'+'\t'+bed_dict_pos[keys]+'\n')
pos_o.close()




def load_data(filename):
    f=open(filename,'r')
    sequences=f.readlines()
    num=len(sequences)
    data=np.empty((num,1000,4),dtype='float32')
    label=np.empty((num,),dtype="int")
    for i in range(num):
        line=sequences[i].replace('\n','')
        list_line=re.split('\s+',line)
        one_sequence=list_line[1]
        for j in range(1000):
            if j<=len(one_sequence)-1:
                if re.findall(one_sequence[j],'A|a'):
                    data[i,j,:]=np.array([1.0,0.0,0.0,0.0],dtype='float32')
                if re.findall(one_sequence[j],'C|c'):
                    data[i,j,:]=np.array([0.0,1.0,0.0,0.0],dtype='float32')
                if re.findall(one_sequence[j],'G|g'):
                    data[i,j,:]=np.array([0.0,0.0,1.0,0.0],dtype='float32')
                if re.findall(one_sequence[j],'T|t'):
                    data[i,j,:]=np.array([0.0,0.0,0.0,1.0],dtype='float32')
                if re.findall(one_sequence[j],'N|n'):
                    data[i,j,:]=np.array([0.0,0.0,0.0,0.0],dtype='float32')
            else:
                data[i,j,:]=np.array([0.0,0.0,0.0,0.0],dtype='float32')
        label[i]=list_line[0]
    return data,label

pos_sample=args.out+"pos.txt"


data_pos,label_pos = load_data(pos_sample)

np.save('data_predict.npy',data_pos)
np.save('label_predict.npy',label_pos)



