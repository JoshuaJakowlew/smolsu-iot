import os
import json
import drawsvg as draw
import numpy as np

DUMPER_PATH = 'ultra_simple.exe'
DUMP_PATH = 'points.json'

DUMPER_CMD = f'{DUMPER_PATH} > {DUMP_PATH}'

print(DUMPER_CMD)
cwd = os.getcwd()
DUMPER_CMD = f'{cwd}\\{DUMPER_PATH} > {cwd}\\{DUMP_PATH}'
os.system(DUMPER_CMD)

with open(f'{cwd}\\{DUMP_PATH}') as dump:
    points = json.load(dump)['points']

def pol2cart(rho, phi):
    x = rho * np.cos(np.deg2rad(phi))
    y = rho * np.sin(np.deg2rad(phi))
    return(x, y)

for p in points:
    rho = p['dist']
    phi = p['theta']

import cv2 as cv

points = list(filter(lambda p: p['dist'] > 0.0, points))
points.sort(key=lambda p: p['theta'])
coords = [pol2cart(p['dist'], p['theta']) for p in points]

coords = [(x / 20, y / 20) for x, y in coords]

x_min = min(coords, key=lambda p: p[0])[0]
x_max = max(coords, key=lambda p: p[0])[0]

y_min = min(coords, key=lambda p: p[1])[1]
y_max = max(coords, key=lambda p: p[1])[1]

w = abs(x_min) + abs(x_max)
h = abs(y_min) + abs(y_max)

print(x_min, x_max, y_min, y_max)

coords = [(x + abs(x_min) + 10, y + abs(y_min) + 10) for x, y in coords]

x_min = min(coords, key=lambda p: p[0])[0]
x_max = max(coords, key=lambda p: p[0])[0]

y_min = min(coords, key=lambda p: p[1])[1]
y_max = max(coords, key=lambda p: p[1])[1]

w = abs(x_min) + abs(x_max)
h = abs(y_min) + abs(y_max)

coords = np.array(coords, dtype=np.int32)

drawing = np.zeros([int(h) + 11, int(w) + 11], np.uint8)

cv.drawContours(drawing, [coords], 0, (255, 255, 255), 1)

kernel = np.ones((5, 5), np.uint8)

drawing = cv.GaussianBlur(drawing, (kernel.shape[0], kernel.shape[1]), 3)
cv.threshold(drawing, 1, 255, cv.THRESH_BINARY, dst=drawing)
# drawing = cv.dilate(drawing, kernel, iterations=1)
drawing = cv.erode(drawing, kernel, iterations=1)

(cnts, _) = cv.findContours(drawing.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

vector = np.zeros([int(h) + 1, int(w) + 1], np.uint8)
cv.drawContours(vector, cnts, 0, (255, 255, 255), 1)

# cv.erode(drawing,)
# cv.imshow('sfdsf', drawing)
# cv.imshow('vector', vector)
# cv.waitKey(0)
from random import randint
cv.imwrite(f'{cwd}\\media\\png\\image{randint(0, 10000000-7)}.png', vector)


d = draw.Drawing(w, h, origin=(0, 0))
d.set_pixel_scale(1)
p = draw.Path(stroke_width=2, stroke='lime', fill='black', fill_opacity=0)

x, y = cnts[0][0][0][0], cnts[0][0][0][1]
p.M(x, y)
for c in cnts[0]:
    p.L(c[0][0], c[0][1])
d.append(p)
d.save_svg(f'{cwd}\\media\\svg\\image{randint(0, 10000000-7)}.svg')

