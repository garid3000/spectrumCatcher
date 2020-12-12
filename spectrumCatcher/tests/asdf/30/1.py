import numpy as np
import matplotlib.pyplot as plt
import os
import time
from PIL import Image

fig = plt.figure()
# ax = fig.add_subplot(111)


coords = []

def onclick(event):
    print(event.xdata, event.ydata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
#plt.show()

image = Image.open('x.jpg')

img =  np.array(image)#plt.imread("x.jpg")
plt.imshow(img)
plt.show()
