import matplotlib as plt
import numpy as np
import pandas as pd

from hometask.dot import Dot
from hometask.task_2 import get_optimal_clusters
from hometask.task_2 import show_clusters
from hometask.task_2 import generate_dots


def euclidean_dist(a: Dot, b: Dot):
    pow_x = np.math.pow(np.math.fabs(a.x - b.x), 2)
    pow_y = np.math.pow(np.math.fabs(a.y - b.y), 2)
    return np.math.sqrt(pow_x + pow_y)


n = 250
e = 3
dots = generate_dots(n, 60, 60)
clusters = get_optimal_clusters(dots)
show_clusters(clusters)

k = len(clusters.keys())
print("k = ", k)

weight = np.random.dirichlet(np.ones(k), size=n)
# print(weight)

centers = clusters.keys()
print("centers = ", centers)
center_dots = []
for c in centers:
    center_dots.append(c)
print("center dots = ", center_dots)

centroids = []
for i in range(k):
    centroids.append(Dot(0, 0))

p = 2
m_new = 0
m_old = 0
while m_new == 0 or np.math.fabs(m_new - m_old) > e:

    m_old = m_new

    for j in range(k):
        nom_sum_x = 0
        nom_sum_y = 0
        deno_sum = 0
        for i in range(n):
            pow_sum = np.math.pow(weight[i, j], p)
            nom_sum_x += pow_sum * dots[i].x
            nom_sum_y += pow_sum * dots[i].y
            deno_sum += pow_sum
        centroids[j] = Dot(nom_sum_x / deno_sum, nom_sum_y / deno_sum)

    for ii in range(n):
        deno_val = 0
        for jj in range(k):
            deno_val += np.math.pow(1 / euclidean_dist(dots[ii], centroids[jj]), 1 / (p - 1))
        for jj in range(k):
            new_w = np.math.pow(1 / euclidean_dist(dots[ii], centroids[jj]), 1 / (p - 1)) / deno_val
            weight[ii, jj] = new_w

    m_new = 0
    for j in range(k):
        for i in range(n):
            m_new += np.math.pow(weight[i, j], p) * euclidean_dist(dots[i], centroids[j])

print("new centroids = ", centroids)

new_clusters = {}
for j in range(k):
    new_clusters.update({centroids[j]: []})
for i in range(n):
    max_w = max(weight[i, :])
    idx = np.where(weight[i] == max_w)[0][0]
    curr_array = new_clusters.get(centroids[idx])
    curr_array.append(dots[i])
    new_clusters.update({centroids[idx]: curr_array})

show_clusters(new_clusters)
