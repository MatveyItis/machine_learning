import numpy as np
import matplotlib.pyplot as plt
import random


class Dot:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return 'x=' + str(self.x) + ' ' + 'y=' + str(self.y)

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))


def show_dots(dots: []):
    x = []
    y = []
    for o in range(0, len(dots)):
        x.append(dots[o].x)
        y.append(dots[o].y)
    plt.scatter(x, y)
    plt.show()


def show_clusters(clusters: {}):
    colors = ["red", "green", "blue", "black", "pink"]
    i = 0
    for k in clusters.keys():
        dots = clusters.get(k)
        x = [k.x]
        y = [k.y]
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
        d = Dot(random.randint(0, max_x), random.randint(0, max_y))
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
    clusters = create_clusters(dots.copy(), centers.copy())
    new_centers = re_center(clusters)
    while centers != new_centers:
        clusters = create_clusters(dots.copy(), new_centers.copy())
        centers = new_centers
        new_centers = re_center(clusters)
    return clusters


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
        c_x = c_x / len(cluster_dots)
        c_y = c_y / len(cluster_dots)
        new_clusters.append(Dot(x=c_x, y=c_y))
    return new_clusters


rand_dots = generate_dots(150, 100, 100)
show_dots(rand_dots)

res_clusters = get_final_clusters(rand_dots, 3)
show_clusters(res_clusters)
#
# center_dots = get_centers(rand_dots, 3)
# show_dots(center_dots)
