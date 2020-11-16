import pygame
import sys
from sklearn import svm
import numpy as np


def get_color(button_value):
    if button_value == 1:
        return RED
    if button_value == 3:
        return BLUE
    else:
        return GREEN


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)

pygame.init()
sc = pygame.display.set_mode((800, 600))
sc.fill(WHITE)
pygame.display.update()

clock = pygame.time.Clock()

cluster_dots = {}
control_dots = []
clf = svm.SVC()

is_model_ready = False
play = True
while play:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            play = False
            pygame.quit()
            sys.exit(0)
        if i.type == pygame.MOUSEBUTTONDOWN:
            b_val = i.button
            if b_val == 1 or b_val == 3:
                color = get_color(b_val)
                if not is_model_ready:
                    if cluster_dots.get(color) is None:
                        cluster_dots.update({color: []})
                    arr = cluster_dots.get(color)
                    arr.append([i.pos[0], i.pos[1]])
                    cluster_dots.update({color: arr})
                    pygame.draw.circle(sc, color, i.pos, 10)
                    pygame.display.update()
                else:
                    print("Add control dots")
                    control_dots.append([i.pos[0], i.pos[1]])
                    pygame.draw.circle(sc, color, i.pos, 10)
                    pygame.display.update()
        if i.type == pygame.KEYDOWN:
            if i.key == 32:
                print("Start svm algorithm")
                x1 = cluster_dots.get(RED)
                print("red array = ", x1)
                y = []
                for j in range(0, len(x1)):
                    y.append(0)
                x2 = cluster_dots.get(BLUE)
                print("blue array = ", x2)
                for j in range(0, len(x2)):
                    y.append(1)
                print("y array = ", y)
                x = []
                for j in range(0, len(x1)):
                    x.append(x1[j])
                for j in range(0, len(x2)):
                    x.append(x2[j])
                print("x array = ", x)
                clf.fit(x, y)
                print("Model has been fitted")
                is_model_ready = True
            if i.key == 107:
                print("Prediction has started")
                prediction = clf.predict(control_dots)
                print(prediction)
    pygame.time.delay(20)
    clock.tick(60)
