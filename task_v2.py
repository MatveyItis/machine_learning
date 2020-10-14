import pandas as pd
import matplotlib.pyplot as plt


def read_csv(file):
    data = pd.read_csv(file)
    return data


def draw(dataset):
    date = list(dataset.Date)
    series = list(dataset['Monthly Mean Total Sunspot Number'])
    plt.figure(figsize=[40, 10])
    plt.plot(date, series)
    plt.scatter(date, series)
    # plt.xlim(0, 100)
    plt.xlabel("Months since Jan 1749.")
    plt.ylabel("No. of Sun spots")
    n = 25
    result = pd.DataFrame(series)
    rolling_mean = result.rolling(window=n).mean()
    plt.plot(rolling_mean, color='r')
    plt.show()


data = read_csv('data/sunspots.csv')
draw(data)
