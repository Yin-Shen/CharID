for i in chr*_predict.bed
do
cat >${i%%_*}_predict.py<<EOF
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN



def cluster(indices: np.ndarray,
            contacts: np.ndarray, dis=100, min_samples=2, **kwargs):
    dbscan = DBSCAN(eps=dis, min_samples=min_samples, **kwargs)
    dbscan.fit(indices.T)

    peak_indexs, shapes, members = [], [], []
    for cluster_id in set(dbscan.labels_) - {-1}:
        point_indexs = np.where(dbscan.labels_ == cluster_id)[0]
        points = indices[:, point_indexs]
        center_index = np.argmax(contacts[point_indexs])
        center = points[:, center_index]
        width = np.abs(points[1] - center[1]).max() * 2 + 1
        height = np.abs(points[0] - center[0]).max() * 2 + 1
        peak_indexs.append(point_indexs[center_index])
        members.append(point_indexs)
        if height >= 2 * width:
            height = width
        elif width >= 2 * height:
            width = height
        shapes.append([width, height])

    for singlet_index in np.where(dbscan.labels_ == -1)[0]:
        peak_indexs.append(singlet_index)
        shapes.append([1, 1])
        members.append([singlet_index])

    return np.array(peak_indexs), np.array(shapes).T, members

df = pd.read_csv('$i', delimiter='\t', header=None)
df = df[[1,2,4,5]].astype(int) / 1000
df['a'] = df[[1, 2]].sum(axis=1) / 2
df['b'] = df[[4, 5]].sum(axis=1) / 2
indices = np.array(df[['a', 'b']]).T
contacts = np.ones(len(indices.T))

a, b, c = cluster(indices, contacts)
loops_pool = []
for line in open('$i', 'r'):
    loops_pool.append(line)
loops_out = []
for i in a:
    loops_out.append(loops_pool[int(i)])
o=open("cluster_${i%%_*}.bed", 'w')
o.write(''.join(loops_out))
o.close()


EOF
done    
