import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_simple_dots():
    return [(np.random.randint(low=0, high=150), np.random.randint(low=0, high=150)) for i in range(100)]


def show_init_dataframe(X, Y):
    plt.scatter(X, Y)
    plt.show()


def show_line(X, Y, y_pred):
    plt.scatter(X, Y)
    plt.plot([min(X), max(X)], [min(y_pred), max(y_pred)], color='black')
    plt.show()


if __name__ == '__main__':
    m = 0
    c = 0
    L = 0.0001
    epochs = 1000
    gen_dots = generate_simple_dots()
    frame = pd.DataFrame(gen_dots)
    X = frame.iloc[:, 0]
    Y = frame.iloc[:, 1]
    show_init_dataframe(X, Y)
    n = float(len(X))
    for i in range(epochs):
        y_pred = m * X + c
        d_m = (-2 / n) * sum(X * (Y - y_pred))
        d_c = (-2 / n) * sum(Y - y_pred)
        m = m - L * d_m
        c = c - L * d_c
    # Predict
    y_pred = m * X + c
    show_line(X, Y, y_pred)
