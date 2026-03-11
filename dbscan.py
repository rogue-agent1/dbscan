#!/usr/bin/env python3
"""DBSCAN density-based clustering."""
import sys, math, random
random.seed(42)
def dist(a,b): return math.hypot(a[0]-b[0],a[1]-b[1])
def dbscan(pts,eps,min_pts):
    labels=[-1]*len(pts); c=0
    for i in range(len(pts)):
        if labels[i]!=-1: continue
        neighbors=[j for j in range(len(pts)) if dist(pts[i],pts[j])<=eps]
        if len(neighbors)<min_pts: continue
        labels[i]=c; seed=list(neighbors)
        while seed:
            q=seed.pop()
            if labels[q]==-1 or labels[q]==-2: labels[q]=c
            if labels[q]!=-1 and labels[q]!=c: continue
            qn=[j for j in range(len(pts)) if dist(pts[q],pts[j])<=eps]
            if len(qn)>=min_pts: seed+=qn
        c+=1
    return labels
pts=[(random.gauss(0,1),random.gauss(0,1)) for _ in range(20)]
pts+=[(random.gauss(5,1),random.gauss(5,1)) for _ in range(20)]
pts+=[(random.gauss(10,0.5),random.gauss(0,0.5)) for _ in range(10)]
labels=dbscan(pts,2,3)
clusters=max(labels)+1; noise=labels.count(-1)
print(f"DBSCAN: {clusters} clusters, {noise} noise points")
for c in range(clusters):
    members=[pts[i] for i in range(len(pts)) if labels[i]==c]
    cx=sum(p[0] for p in members)/len(members); cy=sum(p[1] for p in members)/len(members)
    print(f"  Cluster {c}: {len(members)} points, center=({cx:.1f},{cy:.1f})")
