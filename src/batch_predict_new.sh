#! /bin/bash
cd ../result
MAXINDEX=`ls predict_ocr_loop*.py |wc -l`
File=`ls predict_*.txt 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
    File=`ls predict_*.txt 2>/dev/null |wc -w`
    sleep 10
done
if [ $File = ${MAXINDEX} ]
then
for i in `ls predict_*.txt`
do
cat>whole_${i%%.txt*}.py<<EOF

genome=[]
genome_line=0
for l in open('predict_ocr_loop`echo $i | tr -cd "[0-9]"`','r'):
    if l.startswith('chrom1'):
       continue
    else:
        ll=l.strip().split()
        genome.append('\t'.join(ll[:6]))
        genome_line +=1

predict=[]
value = []
for line in open('$i','r'):
    lines=line.strip().split()
    predict.append(lines[0])
    value.append(lines[1])
genome_pre={}
genome_value={}
lines=0
while lines < genome_line:
    k_name=genome[lines]
    genome_pre[k_name]=predict[lines]
    genome_value[k_name]=value[lines]
    lines+=1

o=open('whole_pre_`echo $i | tr -cd "[0-9]"`.txt','w')
for k,v in genome_pre.items():
    if genome_pre[k] == '1':
        o.write(k+'\t'+str(genome_value[k])+'\n')
o.close()

EOF
done
fi
