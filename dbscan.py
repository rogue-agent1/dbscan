#!/usr/bin/env python3
"""dbscan - DBSCAN density-based clustering."""
import sys,math,random
def dist(a,b):return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
def region_query(data,p,eps):return[i for i,q in enumerate(data) if dist(data[p],q)<=eps]
def dbscan(data,eps=1.0,min_pts=5):
    n=len(data);labels=[-1]*n;cluster=-1
    for i in range(n):
        if labels[i]!=-1:continue
        neighbors=region_query(data,i,eps)
        if len(neighbors)<min_pts:labels[i]=-2;continue
        cluster+=1;labels[i]=cluster;seed=list(neighbors)
        while seed:
            q=seed.pop()
            if labels[q]==-2:labels[q]=cluster
            if labels[q]!=-1:continue
            labels[q]=cluster;qn=region_query(data,q,eps)
            if len(qn)>=min_pts:seed.extend(qn)
    return labels
if __name__=="__main__":
    random.seed(42);data=[]
    for cx,cy in[(0,0),(6,6),(12,0)]:data.extend([(cx+random.gauss(0,1),cy+random.gauss(0,1)) for _ in range(30)])
    data.extend([(random.uniform(-5,17),random.uniform(-5,11)) for _ in range(10)])
    labels=dbscan(data,eps=2.0,min_pts=3)
    clusters=set(l for l in labels if l>=0);noise=sum(1 for l in labels if l<0)
    print(f"Points: {len(data)}, Clusters: {len(clusters)}, Noise: {noise}")
    for c in sorted(clusters):pts=sum(1 for l in labels if l==c);print(f"  Cluster {c}: {pts} points")
