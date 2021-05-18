# Import libraries
import math
import numpy as np
import matplotlib.pyplot as plt
import csv

odmX = []
odmY = []
odmW = []

with open('robotOdm_clear.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Column names are ", ", ".join(row))
            line_count += 1
        else:
            odmX.append(row[1])
            odmY.append(row[2])
            odmW.append(row[3])
            line_count += 1
    print('Processed {0} lines.'.format(line_count))


fig, ax = plt.subplots()


ax.quiver(odmX, odmY, odmX+math.cos(odmW), odmY+math.sin(odmW))
ax.set_title('Quiver plot with one arrow')


plt.show()
  
# # Creating grids
# X, Y = np.meshgrid(x, y)
  
# # x-component to the right
# u = np.ones((10, 10)) 
  
# # y-component zero
# v = np.zeros((10, 10)) 
  
# fig = plt.figure(figsize = (12, 7))
  
# # Plotting stream plot
# plt.streamplot(X, Y, u, v, density = 0.5)
  
# # show plot
# plt.show()
