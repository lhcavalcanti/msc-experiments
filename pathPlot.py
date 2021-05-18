# Import libraries
import numpy as np
import matplotlib.pyplot as plt
  
# Creating dataset
x = np.arange(0, 10)
y = np.arange(0, 10)
  
# Creating grids
X, Y = np.meshgrid(x, y)
  
# x-component to the right
u = np.ones((10, 10)) 
  
# y-component zero
v = np.zeros((10, 10)) 
  
fig = plt.figure(figsize = (12, 7))
  
# Plotting stream plot
plt.streamplot(X, Y, u, v, density = 0.5)
  
# show plot
plt.show()