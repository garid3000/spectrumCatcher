import numpy as np
import matplotlib.pyplot as plt
import os
import time

x = np.arange(-10,10)
y = x**2

fig = plt.figure()
ax = fig.add_subplot(111)
state = True
#ax.plot(x,y)

coords = []

def onclick(event):
    if event.button == 1:
        global ix, iy, state
        ix, iy = event.xdata, event.ydata
        print ('x = %d, y = %d'%(ix, iy))

        global coords
        coords.append((ix, iy))

        if len(coords) == 4:
            fig.canvas.mpl_disconnect(cid)
        return coords
    else:
        global  state
        print("none")
        state = False
        print(state)
        fig.canvas.mpl_disconnect(cid)
        pass

cid = fig.canvas.mpl_connect('button_press_event', onclick)
#plt.show()

files = ["20201211/"+file for file in os.listdir("20201211") if "jpg" in file]

for file in files:
    img =  plt.imread(file)
    ax.imshow(img)
    plt.show()
    state = True
    while 1:
        print(state)
        if state:
            pass
        else:
            break
        time.sleep(0.1)
