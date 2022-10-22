import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()  # Create a figure containing a single axes.
ax = fig.add_subplot(111, projection="3d")

ax.plot([1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 6])
ax.plot([2, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 6])

plt.show()
