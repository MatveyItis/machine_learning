from math import hypot
import numpy as np

from hometask.task_2 import show_clusters
from hometask.dot import Dot

eps = 20
m = 2
not_neighbor_key = -1


def euclidean_dist(a: Dot, b: Dot):
    pow_x = np.math.pow(np.math.fabs(a.x - b.x), 2)
    pow_y = np.math.pow(np.math.fabs(a.y - b.y), 2)
    return np.math.sqrt(pow_x + pow_y)


def get_neighbors(p):
    return [q for q in dots if euclidean_dist(p, q) < eps]


def form_cluster_dots(clusters: {}, cluster_num, visited_dots, clustered_dots, p, neighbors):
    if cluster_num not in clusters:
        clusters.update({cluster_num: []})
    curr_array = clusters.get(cluster_num)
    curr_array.append(p)
    clusters.update({cluster_num: curr_array})
    clustered_dots.add(p)
    while neighbors:
        q = neighbors.pop()
        if q not in visited_dots:
            visited_dots.add(q)
            neighbor_q = get_neighbors(q)
            if len(neighbor_q) > m:
                neighbors.extend(neighbor_q)
        if q not in clustered_dots:
            clustered_dots.add(q)
            q_curr_array = clusters.get(cluster_num)
            q_curr_array.append(q)
            clusters.update({cluster_num: q_curr_array})
            if q in clusters.get(not_neighbor_key):
                remove_arr = clusters.get(not_neighbor_key)
                remove_arr.remove(q)
                clusters.update({cluster_num: remove_arr})


def db_scan(dots: []):
    cluster_num = 0

    visited_dots = set()
    clustered_dots = set()
    clusters = {not_neighbor_key: []}

    for dot in dots:
        if dot not in visited_dots:
            visited_dots.add(dot)
            neighbors = get_neighbors(dot)
            if len(neighbors) < m:
                not_neighbor_array = clusters.get(not_neighbor_key)
                not_neighbor_array.append(dot)
                clusters.update({not_neighbor_key: not_neighbor_array})
            else:
                cluster_num += 1
                form_cluster_dots(clusters, cluster_num, visited_dots, clustered_dots, dot, neighbors)
    return clusters


def generate_diff_dots(n, x_low, x_high, y_low, y_high):
    return [Dot(np.random.randint(low=x_low, high=x_high), np.random.randint(low=y_low, high=y_high)) for i in range(n)]


if __name__ == '__main__':
    n = 300
    dots = generate_diff_dots(n, 0, 45, 0, 55)
    dots.extend(generate_diff_dots(n, 60, 110, 60, 110))

    clusters = db_scan(dots)
    print("clusters keys size = ", len(clusters.keys()) - 1)
    show_clusters(clusters)
