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


def get_centers(dots: [], k: int):
    max_distance = 0
    c_1: Dot = None
    c_2: Dot = None
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


rand_dots = generate_dots(200, 100, 100)
show_dots(rand_dots)

center_dots = get_centers(rand_dots, 3)
show_dots(center_dots)
