import pandas as pd
import matplotlib.pyplot as plt


def read_csv(file):
    data = pd.read_csv(file)
    return data


def draw(dataset):
    date = list(dataset.Date)
    emession = list(dataset['Monthly Mean Total Sunspot Number'])
    emession_new = []
    emession_new[0] = emession[0]
    for i in range(1, len(emession) - 1):
        emession_new[i] = (emession[i - 1] * i + emession[i]) / (i + 1)

    plt.figure(figsize=[30, 10])
    plt.plot(date, emession, color='r')
    plt.scatter(date, emession)
    # plt.xlim(0, 100)
    plt.show()


data = read_csv('data/sunspots.csv')
draw(data)
