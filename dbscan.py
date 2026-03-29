#!/usr/bin/env python3
"""DBSCAN density-based clustering from scratch."""
import sys, math, random

def distance(a, b): return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))

def dbscan(data, eps=0.5, min_pts=5):
    n = len(data); labels = [-1] * n; cluster_id = 0
    visited = [False] * n

    def region_query(idx):
        return [j for j in range(n) if distance(data[idx], data[j]) <= eps]

    def expand_cluster(idx, neighbors, cid):
        labels[idx] = cid; i = 0
        while i < len(neighbors):
            nb = neighbors[i]
            if not visited[nb]:
                visited[nb] = True
                nb_neighbors = region_query(nb)
                if len(nb_neighbors) >= min_pts:
                    neighbors.extend([x for x in nb_neighbors if x not in neighbors])
            if labels[nb] == -1: labels[nb] = cid
            i += 1

    for i in range(n):
        if visited[i]: continue
        visited[i] = True
        neighbors = region_query(i)
        if len(neighbors) < min_pts: labels[i] = -1  # noise
        else:
            expand_cluster(i, neighbors, cluster_id)
            cluster_id += 1

    return labels, cluster_id

def main():
    random.seed(42)
    # Generate clustered data with noise
    data = []
    for cx, cy, r, count in [(0,0,0.5,30), (3,3,0.5,30), (6,0,0.5,30)]:
        for _ in range(count):
            angle = random.uniform(0, 2*math.pi)
            radius = random.gauss(0, r)
            data.append([cx + radius*math.cos(angle), cy + radius*math.sin(angle)])
    # Add noise
    for _ in range(10): data.append([random.uniform(-2, 8), random.uniform(-2, 5)])

    labels, n_clusters = dbscan(data, eps=1.0, min_pts=3)
    noise = labels.count(-1)
    print(f"DBSCAN: {n_clusters} clusters found, {noise} noise points")
    from collections import Counter
    counts = Counter(labels)
    for cid in sorted(counts):
        name = f"Cluster {cid}" if cid >= 0 else "Noise"
        print(f"  {name}: {counts[cid]} points")

if __name__ == "__main__": main()
