import pandas as pd
import matplotlib.pyplot as plt


def read_csv(file):
    data = pd.read_csv(file)
    return data


def draw(dataset):
    ages = list(dataset.Age)
    survived = list(dataset.Survived)
    y = []
    colors = []
    for i in range(0, len(ages)):
        y.append(i + 1)
        if survived[i] == 0:
            colors.append('r')
        else:
            colors.append('g')
    plt.figure(figsize=[20, 10])
    plt.bar(y, ages, color=colors)
    plt.xlim(0, 300)
    plt.show()


data = read_csv('data/titanic/train.csv')
draw(data)
