for i in chr*_predict.bed
do
cat >${i%%_*}_predict.py<<EOF
from __future__ import  division
import numpy as np
import  math
loopType = [ ('chr1', '<U7'), ('S1', '<i4'), ('E1', '<i4'), ('chr2', '<U7'), ('S2', '<i4'), ('E2', '<i4'),('P', '<f8')]
loops = np.loadtxt('$i', dtype = loopType)
def center_sites(lists):
    sum_x = 0
    sum_y = 0
    for x in lists:
        sum_x += int(x[1])
        sum_y += int(x[5])
    n = len(lists)
    return [float(sum_x)/n, float(sum_y)/n]
	
def distance(sites_1,sites_2):
    dis = math.sqrt((sites_1[0]-int(sites_2[1]))**2 + (sites_1[1]-int(sites_2[5]))**2)
    return dis

def removearray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind],arr):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')


def clustering(loop_sites, dis):
        classes = []
        c_loops = sorted(loop_sites[loop_sites['chr1'] == '${i%%_*}'], key = lambda x:int(x[1]))
        while True :
            c_classs = []
            c_classs.append(c_loops[0])
            removearray(c_loops, c_loops[0])
            center = center_sites(c_classs)
            for loop in c_loops:     
                 if distance(center, loop) <= dis:
                      c_classs.append(loop)
                      center = center_sites(c_classs)
                      removearray(c_loops, loop)
            classes.append(c_classs)
            if len(c_loops) == 0:
                break
        return classes
	
def filtering(cls):
    loop = []
    for outs in cls:
        lens = len(outs)
        if  lens >= 2 :
            outs = sorted(outs, key=lambda x:int(x[6]))
            loop.append(outs[0])
        else:
            loop.append(outs[0])
    return np.array(loop, dtype = loopType)

initial_distance = 20000	
cluster_1 = clustering(loops, initial_distance)
loops2 = []
for outs in cluster_1:
    lens = len(outs)
    if lens >= 2 :
        outs = sorted(outs, key=lambda x:int(x[6]))
        loops2.append(outs[0])
loops_in = np.array(loops2, dtype = loopType)
while True:
    cluster_loop = clustering(loops_in, initial_distance * 2)
    loops_out = filtering(cluster_loop)
    if len(loops_in) == len(loops_out):
        break
    loops_in = loops_out    
np.savetxt("cluster_${i%%_*}.bed", loops_out, fmt='%s', delimiter='\t')
EOF
done    
