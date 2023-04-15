import numpy as np
import matplotlib.pyplot as plt

import json

path = 'results/Calibration/22-11-16-find_params/2-9-no-limits'
with open(path+'/grid_search.json', 'r') as f:
  data = json.load(f)


C_1 = np.array([elm["c1"] for elm in data])
C_2 = np.array([elm["c2"] for elm in data])
W = np.array([elm["w"] for elm in data])
best_cost = np.array([elm["best_cost"] for elm in data])
# print(C_1, C_2, W, best_cost)

print("Best cost mean: ", best_cost.mean())

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Plot the 3D surface
img = ax.scatter(C_1, C_2, W, c=best_cost, cmap=plt.hot())

ax.set(xlim=(0.1, 1), ylim=(0.1, 1), zlim=(0.1, 1), xlabel='C1', ylabel='C2', zlabel='W')
plt.colorbar(img)
plt.show()

fig.savefig(path+"/graph", dpi=500)