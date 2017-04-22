import cv2
import numpy as np

img = cv2.imread('01.jpg')

# Average RGB
avg = [0, 0, 0]
for x, line in enumerate(img):
   for y, px in enumerate(line):
      avg[0] += img[x][y][0]
      avg[1] += img[x][y][1]
      avg[2] += img[x][y][2]
print(avg)
avg = np.divide(avg, (len(img) * len(img[0])))
print(avg)
