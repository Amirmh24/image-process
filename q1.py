import cv2
import numpy as np

I = cv2.imread("Dark.jpg")
height, width, channels = I.shape
C = np.ones([height, width]) * 5
White = np.ones([height, width]) * 255
for ch in range(0, 3):
    I[:, :, ch] = np.minimum(C * I[:, :, ch], White)
I = cv2.medianBlur(I, 9)
cv2.imwrite("res01.jpg", I)
