import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
# Make data.

out = np.load("outAngle.npy")

X = np.arange(0, 500, 1)
Y = np.arange(0, 800, 1)
X, Y = np.meshgrid(X, Y)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, out, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.show()
