import random
import math
import pylab as pl
import numpy as np
from matplotlib.colors import ListedColormap


def generate_dot(num_class, num_of_classes):
    data = []
    for classNum in range(num_of_classes):
        x, y = random.random() * 5.0, random.random() * 5.0
        for row_num in range(num_class):
            data.append([[random.gauss(x, 0.5), random.gauss(y, 0.5)], classNum])
    return data


def split_train_test(data, test_percent):
    train_data = []
    test_data = []
    for row in data:
        if random.random() < test_percent:
            test_data.append(row)
        else:
            train_data.append(row)
    return train_data, test_data


def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def classify_knn(train_data, test_data, k, num_classes):
    test_labels = []
    for test_point in test_data:
        test_dist = [[dist(test_point, train_data[i][0]), train_data[i][1]] for i in range(len(train_data))]
        stat = []
        for i in range(num_classes):
            stat.append(0)
        for d in sorted(test_dist)[0:k]:
            stat[d[1]] += 1
        test_labels.append(sorted(zip(stat, range(num_classes)), reverse=True)[0][1])
    return test_labels


def generate_test_mesh(train_data):
    arr = [train_data[i][0][0] for i in range(len(train_data))]
    x_min = min(arr) - 1.0
    x_max = max(arr) + 1.0
    y_min = min(arr) - 1.0
    y_max = max(arr) + 1.0
    h = 0.05
    test_x, test_y = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return [test_x, test_y]


def knn(num_classes, size_of_class, k):
    train = generate_dot(size_of_class, num_classes)
    test = generate_test_mesh(train)
    test_mesh = classify_knn(train, zip(test[0].ravel(), test[1].ravel()), k, num_classes)
    class_colormap = ListedColormap(['RED', 'LIME', 'WHITE'])
    test_colormap = ListedColormap(['PINK', 'GREEN', 'GREY'])
    pl.pcolormesh(test[0], test[1],
                  np.asarray(test_mesh).reshape(test[0].shape),
                  cmap=test_colormap, shading='auto')
    pl.scatter([train[i][0][0] for i in range(len(train))],
               [train[i][0][1] for i in range(len(train))],
               c=[train[i][1] for i in range(len(train))],
               cmap=class_colormap)
    pl.show()


if __name__ == '__main__':
    knn(3, 60, 6)
