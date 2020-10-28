import numpy as np
import matplotlib.pyplot as plt
import random

from hometask.dot import Dot


def show_dots(dots: []):
    x = []
    y = []
    for o in range(0, len(dots)):
        x.append(dots[o].x)
        y.append(dots[o].y)
    plt.scatter(x, y)
    plt.show()


def show_clusters(clusters: {}):
    colors = ["red", "green", "blue", "black", "pink", "yellow", "gray", "cyan", "magenta"]
    i = 0
    for k in clusters.keys():
        dots = clusters.get(k)
        x = []
        y = []
        for d in dots:
            x.append(d.x)
            y.append(d.y)
        plt.scatter(x, y, color=colors[i])
        i = i + 1
    plt.show()


def get_distance(dot_a: Dot, dot_b: Dot):
    a = dot_a.x - dot_b.x
    b = dot_a.y - dot_b.y
    return np.math.sqrt(a * a + b * b)


def generate_dots(size, max_x, max_y):
    dots = []
    for j in range(0, size):
        d = Dot(random.randint(0, max_x) - random.randint(0, 3), random.randint(0, max_y) + random.randint(0, 3))
        dots.append(d)
    return dots


def get_centers(dots: [], k: int) -> []:
    max_distance = 0
    c_1 = None
    c_2 = None
    centers = []
    for i in range(0, len(dots)):
        d_1 = dots[i]
        for j in range(i + 1, len(dots)):
            d_2 = dots[j]
            distance = get_distance(d_1, d_2)
            if distance > max_distance:
                max_distance = distance
                c_1 = d_1
                c_2 = d_2

    centers.append(c_1)
    centers.append(c_2)
    dots.remove(c_1)
    dots.remove(c_2)

    for i in range(0, k - len(centers)):
        max_distance = 0
        new_center = None
        for j in range(0, len(dots)):
            dot_from = dots[j]
            min_distance_from = 0
            for l in range(0, len(centers)):
                dot_center = centers[l]
                distance = get_distance(dot_from, dot_center)
                if min_distance_from == 0 or distance < min_distance_from:
                    min_distance_from = distance
            if max_distance < min_distance_from:
                max_distance = min_distance_from
                new_center = dot_from
        centers.append(new_center)
        dots.remove(new_center)

    return centers


def create_clusters(dots: [], centers: []):
    clusters = {}
    for d in dots:
        min_distance = 0
        cluster = None
        for c in centers:
            distance = get_distance(d, c)
            if min_distance == 0 or distance < min_distance:
                min_distance = distance
                cluster = c
                if clusters.get(cluster) is None:
                    clusters.update({cluster: []})
        cluster_dots = clusters.get(cluster)
        cluster_dots.append(d)
        clusters.update({cluster: cluster_dots})
    return clusters


def get_final_clusters(dots: [], k: int):
    centers = get_centers(dots.copy(), k)
    fin_clusters = create_clusters(dots.copy(), centers.copy())
    new_centers = re_center(fin_clusters)
    while centers != new_centers:
        fin_clusters = create_clusters(dots.copy(), new_centers.copy())
        centers = new_centers
        new_centers = re_center(fin_clusters)
    return fin_clusters


def re_center(clusters: {}) -> []:
    centers = clusters.keys()
    new_clusters = []
    for c in centers:
        cluster_dots = clusters.get(c)
        c_x = 0
        c_y = 0
        for cluster_dot in cluster_dots:
            c_x += cluster_dot.x
            c_y += cluster_dot.y
        len_cluster_dots = len(cluster_dots)
        c_x = c_x / len_cluster_dots
        c_y = c_y / len_cluster_dots
        new_clusters.append(Dot(x=c_x, y=c_y))
    return new_clusters


def get_distances(clusters: {}):
    summ = 0
    for k in clusters.keys():
        k_dots = clusters.get(k)
        for d in k_dots:
            summ += get_distance(d, k)
    return summ


def calculate_formula_for_the_best_k(distance_keys: [], k: int):
    return np.math.fabs((distance_keys[k - 1] - distance_keys[k]) / (distance_keys[k - 2] - distance_keys[k - 1]))


def get_optimal_clusters(dots: []) -> {}:
    c = 9
    k = 2
    distance_keys = [None] * c
    d = [None] * c
    clusters_keys = [None] * c

    has_next = True
    while has_next:
        clusters_keys[k] = get_final_clusters(dots.copy(), k)
        curr_distance = get_distances(clusters_keys[k])
        distance_keys[k] = curr_distance
        if k > 3:
            d[k - 1] = calculate_formula_for_the_best_k(distance_keys, k)
        k += 1
        has_next = k < c

    filtered_array = []
    for i in range(0, c):
        if d[i] is not None:
            filtered_array.append(d[i])
    idx = d.index(min(filtered_array))
    return clusters_keys[idx]


if __name__ == '__main__':
    rand_dots = generate_dots(400, 100, 100)
    show_dots(rand_dots)
    res_clusters = get_optimal_clusters(rand_dots)
    show_clusters(res_clusters)

#
# center_dots = get_centers(rand_dots, 3)
# show_dots(center_dots)
