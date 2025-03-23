import cv2
import numpy as np

I = cv2.imread("Yellow.jpg")
I = cv2.cvtColor(I, cv2.COLOR_BGR2HSV)
height, width, channels = I.shape
hue = I[:, :, 0]
sat = I[:, :, 1]
val = I[:, :, 2]
I[((20 <= hue) & (hue <= 30))
  & ((-5 * hue + 200 <= sat) & (sat <= -5 * hue + 350))
, 0] = 180
I = cv2.cvtColor(I, cv2.COLOR_HSV2BGR)
cv2.imwrite("res02.jpg", I)

I = cv2.imread("Pink.jpg")
I = cv2.cvtColor(I, cv2.COLOR_BGR2HSV)
height, width, channels = I.shape
hue = I[:, :, 0]
sat = I[:, :, 1]
val = I[:, :, 2]
I[(hue <= 12) | (150 <= hue), 0] = 110
I = cv2.cvtColor(I, cv2.COLOR_HSV2BGR)
cv2.imwrite("res03.jpg", I)
