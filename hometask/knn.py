import random
import math
import pylab as pl
import numpy as np
from matplotlib.colors import ListedColormap


def generate_dot(num_class, numberOfClasses):
    data = []
    for classNum in range(numberOfClasses):
        X, Y = random.random() * 5.0, random.random() * 5.0
        for row_num in range(num_class):
            data.append([[random.gauss(X, 0.5), random.gauss(Y, 0.5)], classNum])
    return data


def split_train_test(data, testPercent):
    train_data = []
    test_data = []
    for row in data:
        if random.random() < testPercent:
            test_data.append(row)
        else:
            train_data.append(row)
    return train_data, test_data


def classify_knn(trainData, testData, k, num_classes):
    def dist(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    test_labels = []
    for testPoint in testData:
        test_dist = [[dist(testPoint, trainData[i][0]), trainData[i][1]] for i in range(len(trainData))]
        stat = [0 for i in range(num_classes)]
        for d in sorted(test_dist)[0:k]:
            stat[d[1]] += 1
        test_labels.append(sorted(zip(stat, range(num_classes)), reverse=True)[0][1])
    return test_labels


def knn(nClasses, nItemsInClass, k):
    def generate_test_mesh(trainData):
        x_min = min([trainData[i][0][0] for i in range(len(trainData))]) - 1.0
        x_max = max([trainData[i][0][0] for i in range(len(trainData))]) + 1.0
        y_min = min([trainData[i][0][1] for i in range(len(trainData))]) - 1.0
        y_max = max([trainData[i][0][1] for i in range(len(trainData))]) + 1.0
        h = 0.05
        testX, testY = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        return [testX, testY]

    train = generate_dot(nItemsInClass, nClasses)
    test = generate_test_mesh(train)
    test_mesh = classify_knn(train, zip(test[0].ravel(), test[1].ravel()), k, nClasses)
    class_colormap = ListedColormap(['#FF0000', '#00FF00', '#FFFFFF'])
    test_colormap = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAAA'])
    pl.pcolormesh(test[0], test[1],
                  np.asarray(test_mesh).reshape(test[0].shape),
                  cmap=test_colormap, shading='auto')
    pl.scatter([train[i][0][0] for i in range(len(train))],
               [train[i][0][1] for i in range(len(train))],
               c=[train[i][1] for i in range(len(train))],
               cmap=class_colormap)
    pl.show()


knn(3, 50, 5)
