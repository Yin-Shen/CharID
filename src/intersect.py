import os
import pybedtools
from pybedtools import BedTool
import pandas as pd
import argparse

#Argument parsing
parser = argparse.ArgumentParser(description='''bedtools intersect''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
parser.add_argument("--bed", "-b", required=True,
                    help="bed file of Chromatin Accessible Regions for input")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()


def merge_whole_loops():    
    whole_loops = open('whole_loops_merge.bed', 'w')
    whole_loops_pool = []
    files = os.listdir(args.dirs+"/loops")
    for file_name in files:
        for line in open(args.dirs+"/loops/"+file_name, 'r'):
            if line not in whole_loops_pool:
                whole_loops_pool.append(line)
            else:
                continue
    whole_loops.write(''.join(whole_loops_pool))
    whole_loops.close()

def intersect(ocr_file, loop_file):
    
    loop_ocr_pool = []
    o_loop_whole = open(args.out+"_whole_old.bed", 'w')
    with open(loop_file, 'r') as f:
        for line in f:
            lines = line.strip().split()
            o_loop_whole.write('\t'.join(str(x) for x in lines[:3])+'\n'+'\t'.join(str(x) for x in lines[3:6])+'\n')
    o_loop_whole.close()
    ocr = pybedtools.BedTool(ocr_file)
    loop_old = pybedtools.BedTool(args.out+"_whole_old.bed").to_dataframe()
    loop_old.drop_duplicates().to_csv(args.out+"_whole.bed", sep='\t', index=False, header=None)
    loop =  BedTool(args.out+"_whole.bed")
    ocr_intersect_loop = ocr.intersect(loop, f=1.0,  output = args.out+"_loop_ocr_old.bed")
    for line in open(args.out+"_loop_ocr_old.bed", 'r'):
        if line not in loop_ocr_pool:
            loop_ocr_pool.append(line)
        else:
            continue
    o_loop_ocr = open(args.out+"_loop_ocr.bed", 'w')
    o_loop_ocr.write(''.join(loop_ocr_pool))
    if os.path.exists(args.out+"_whole_old.bed"):
         os.remove(args.out+"_whole_old.bed")
    else:
         print('no such file:%s'% (args.out+"_whole_old.bed"))
    if os.path.exists(args.out+"_loop_ocr_old.bed"):
         os.remove(args.out+"_loop_ocr_old.bed")
    else:
         print('no such file:%s'% (args.out+"_loop_ocr_old.bed"))    

def split_file(loop_file):
    
    o1 = open(loop_file[:-4]+'_left_final.bed', 'w')
    o2 = open(loop_file[:-4]+'_right_final.bed', 'w')
    with open(loop_file, 'r') as f:
     for i, line in enumerate(f):
        lines = line.split()
        o1.write('\t'.join(lines[:3])+'\t'+str(i+1)+"\n")
        o2.write('\t'.join(lines[3:6])+'\t'+str(i+1)+"\n")
    o1.close()
    o2.close()
           
def ocr_loop(ocr_file, loop_file):
    
    loop_l = pybedtools.BedTool(loop_file[:-4]+'_left_final.bed')
    loop_r = pybedtools.BedTool(loop_file[:-4]+'_right_final.bed')
    ocr_new = open(args.out+'_temp.bed', 'w')
    with open(ocr_file, 'r') as f:
     for i, line in enumerate(f):
        lines = line.split()
        ocr_new.write('\t'.join(lines[:3])+'\t'+str(i+1)+"\n")
    ocr_new.close()
    ocr = pybedtools.BedTool(args.out+'_temp.bed')
    ocr_loopl_pd = ocr.intersect(loop_l, f=1.0, wb = True).to_dataframe()
    ocr_loopr_pd = ocr.intersect(loop_r, f=1.0, wb = True).to_dataframe()
    s1 = pd.merge(ocr_loopl_pd, ocr_loopr_pd, how='inner', on=['thickEnd'])
    s2 = pd.concat([s1.iloc[:,:3], s1.iloc[:, 8:11]], axis=1)
    s3 = s2[s2["chrom_x"] == s2["chrom_y"]]
    s3 = s3.sort_values(by=['chrom_x','start_x','start_y'], axis = 0, ascending=[1,1,1])
    s3 = s3.drop_duplicates()   
    s3['df'] = s3['start_y'] - s3['end_x']
    s4 = s3.loc[(s3['df'] >= 10000) & (s3['df'] <= 2000000)]
    s4 = s4.drop(['df'],axis=1)
    s4.to_csv(args.out+'_ocr_loop.bed',sep='\t', header=None, index=False)
    s4.loc[-1]=['chrom1','start1','end1','chrom2','start2','end2']
    s4.index = s4.index + 1
    s4 = s4.sort_index()
    s4.to_csv(args.out+'_ocr_loop_new.bed',sep='\t', header=None, index=False)
    if os.path.exists(loop_file[:-4]+'_left_final.bed'):
         os.remove(loop_file[:-4]+'_left_final.bed')
    else:
         print('no such file:%s'% (loop_file[:-4]+'_left_final.bed'))
    if os.path.exists(loop_file[:-4]+'_right_final.bed'):
         os.remove(loop_file[:-4]+'_right_final.bed')
    else:
         print('no such file:%s'% (loop_file[:-4]+'_right_final.bed'))
    if os.path.exists(args.out+'_temp.bed'):
         os.remove(args.out+'_temp.bed')
    else:
         print('no such file:%s'% (args.out+'_temp.bed'))

merge_whole_loops()
split_file('whole_loops_merge.bed')
intersect(args.bed, 'whole_loops_merge.bed')
ocr_loop(args.out+'_loop_ocr.bed', 'whole_loops_merge.bed')
