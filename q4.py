import cv2
import matplotlib.pyplot as plt
import numpy as np

I1 = cv2.imread("Dark.jpg")
I2 = cv2.imread("Pink.jpg")
I1 = cv2.cvtColor(I1, cv2.COLOR_BGR2HSV)
I2 = cv2.cvtColor(I2, cv2.COLOR_BGR2HSV)
height1, width1, channels = I1.shape
I2 = cv2.resize(I2, (width1, height1))
height2, width2, channels = I2.shape

fig, p = plt.subplots(1, 3)
for ch in range(channels):
    hist1 = cv2.calcHist([I1], [ch], None, [256], [0, 256])
    hist2 = cv2.calcHist([I2], [ch], None, [256], [0, 256])
    cumHist1 = np.cumsum(hist1)
    cumHist2 = np.cumsum(hist2)
    chnl = I1[:, :, ch]
    chnlTarget = np.zeros([height1, width1])
    besti2 = 0
    for i1 in range(len(cumHist1)):
        print(i1)
        min = float('inf')
        for i2 in range(besti2, len(cumHist2)):
            dist = abs(cumHist1[i1] - cumHist2[i2])
            if (dist <= min):
                min = dist
                besti2 = i2
            else:
                break
        chnlTarget[chnl == i1] = besti2
    I1[:, :, ch] = chnlTarget
    hist1 = cv2.calcHist([I1], [ch], None, [256], [0, 256])
    cumHist1=np.cumsum(hist1)
    # p[ch].plot(cumHist1, color="green")
    # p[ch].plot(cumHist2, color="red")
    p[ch].plot(hist1, color="green")
    if(ch==0):p[ch].set_title("hue")
    if(ch==1):p[ch].set_title("saturation")
    if(ch==2):p[ch].set_title("value")

I1 = cv2.cvtColor(I1, cv2.COLOR_HSV2BGR)
I2 = cv2.cvtColor(I2, cv2.COLOR_HSV2BGR)
fig.set_figheight(6)
fig.set_figwidth(20)
plt.savefig("res05.jpg")
cv2.imwrite("res06.jpg", I1)
