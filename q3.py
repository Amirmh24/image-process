import cv2
import numpy as np


def shift(img, dx, dy):
    hei, wid = img.shape
    padWidth = max(abs(dx), abs(dy))
    dx = dx + padWidth
    dy = dy + padWidth
    padColor = int(img[0, 0])
    img = np.pad(img, pad_width=padWidth, mode='constant', constant_values=padColor)
    img = img[dx:(dx + hei), dy:(dy + wid)]
    return img


def match(img0, img1, img2, sr):
    hei0, wid0 = img0.shape
    padWidth = int(sr)
    padColor = int(img0[0, 0])
    img1 = np.pad(img1, pad_width=padWidth, mode='constant', constant_values=padColor)
    img2 = np.pad(img2, pad_width=padWidth, mode='constant', constant_values=padColor)
    bestdx1 = 0
    bestdy1 = 0
    bestdx2 = 0
    bestdy2 = 0
    min1 = float('inf')
    min2 = float('inf')
    for dx in range(int(sr * 2)):
        for dy in range(int(sr * 2)):
            dist1 = np.sum((img0 - img1[dx:(dx + hei0), dy:(dy + wid0)]) ** 2)
            dist2 = np.sum((img0 - img2[dx:(dx + hei0), dy:(dy + wid0)]) ** 2)
            if (dist1 < min1):
                min1 = dist1
                bestdx1 = dx - padWidth
                bestdy1 = dy - padWidth
            if (dist2 < min2):
                min2 = dist2
                bestdx2 = dx - padWidth
                bestdy2 = dy - padWidth
    return bestdx1, bestdy1, bestdx2, bestdy2


I = np.float64(cv2.imread("melons.tif", -1))
height = int(I.shape[0] / 3)
I0 = I[0:height, :]
height0, width0 = I0.shape
I1 = I[height:2 * height, :]
height1, width1 = I1.shape
I2 = I[2 * height:3 * height, :]
height2, width2 = I2.shape

# shifting parameters
x1 = 0
y1 = 0
x2 = 0
y2 = 0

# searchi range
sr = 30
# pyramid's iteration
r = 8
# hop
x = 2
# resizing ratio
rr = x ** (r - 1)

for i in range(r):
    # keep I0 static but I1 and I2 dynamic
    I0Scaled = cv2.resize(I0, (int(width0 / rr), int(height0 / rr)))
    I1Scaled = shift(cv2.resize(I1, (int(width1 / rr), int(height1 / rr))), x1 * x, y1 * x)
    I2Scaled = shift(cv2.resize(I2, (int(width2 / rr), int(height2 / rr))), x2 * x, y2 * x)
    dx1, dy1, dx2, dy2 = match(I0Scaled, I1Scaled, I2Scaled, sr)
    x1 = x1 * x + dx1
    y1 = y1 * x + dy1
    x2 = x2 * x + dx2
    y2 = y2 * x + dy2
    print(i)
    rr = int(rr / x)
    sr = x

I = np.zeros((height0, width0, 3))
I[:, :, 0] = I0Scaled
I[:, :, 1] = I1Scaled
I[:, :, 2] = I2Scaled

I = cv2.normalize(I, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
cv2.imwrite("res04.jpg", I)
