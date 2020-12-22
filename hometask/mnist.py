import matplotlib.pyplot as plt
import numpy as np
import pygame as pg
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D
import matplotlib.image as mpimg
import cv2
import random
from IPython.display import Image

(X_train, y_train), (X_test, y_test) = mnist.load_data()


def show_mnist_samples(image_data, label_data, classes, N=8):
    plt.figure(figsize=(10, N))
    num_classes = len(classes)
    for i, y in enumerate(classes):
        idxs = np.flatnonzero(label_data == y)
        idxs = np.random.choice(idxs, N, replace=False)
        for i, idx in enumerate(idxs):
            plt_idx = i * num_classes + y + 1
            plt.subplot(N, num_classes, plt_idx)
            plt.imshow(image_data[idx], cmap='gray')
            plt.axis('off')
            if i == 0:
                plt.title(str(y))
    plt.show()


classes = list(range(0, 10))
show_mnist_samples(X_train, y_train, classes)

X_train = X_train / 255
X_test = X_test / 255

y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

X_train, X_test = X_train.reshape((60000, 28, 28, 1)), X_test.reshape((10000, 28, 28, 1))
input_size = X_train[0].shape

conv_model = Sequential()
conv_model.add(Conv2D(24, (3, 3), padding='same', input_shape=input_size))
conv_model.add(Activation('relu'))
conv_model.add(Flatten())
conv_model.add(Dense(64, activation='relu'))
conv_model.add(Dense(10, activation='softmax'))

conv_model.summary()

conv_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
conv_model.fit(X_train, y_train, epochs=6, batch_size=32)


def get_prediction():
    img = mpimg.imread('picture.png')[..., 1]
    img = cv2.resize(img, dsize=(28, 28))
    img = np.array(img).reshape(1, 28, 28, 1)
    predict = conv_model.predict(img)
    return np.argmax(predict, axis=1)[0]


def airbrush():
    cur = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if click[0]:
        pg.draw.circle(sc, WHITE, (cur[0] + random.randrange(2), cur[1] + random.randrange(2)), random.randrange(1, 6))


pg.init()
sc = pg.display.set_mode((400, 300))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
sc.fill(BLACK)
pg.display.update()
f1 = pg.font.Font(None, 36)

play = True
while play:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            play = False
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 3:
                pg.image.save(sc, '../picture.png')
                dog_surf = pg.image.load('../picture.png')
                pred = get_prediction()
                text1 = f1.render('Предсказанная цифра: {0}'.format(pred), True, WHITE)
                sc.blit(text1, (10, 10))
                pg.display.update()
        if i.type == pg.KEYDOWN:
            print('hey in key if, val = ', i.key)
            if i.key == 32:
                print('hey in space key')
                sc.fill(BLACK)
                pg.display.update()
    if play:
        airbrush()
        pg.display.update()

Image("предсказание.png")
