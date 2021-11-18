# Import libraries
import math
import csv
import numpy as np
import matplotlib.pyplot as plt

version = 'calibration-test1-S'
robotFile = 'data/Calibration/10-11-2021/Teste 1/test-1-S-logs-2021-11-09.10:51:47.csv'

odm = []
vis = []
comp = []

with open(robotFile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Column names are ", ", ".join(row))
            line_count += 1
        else:
            odm.append([float(row[1]), float(row[2]), float(row[3])])
            vis.append([float(row[8]), float(row[9]), float(row[10])])
            # GYRO_W, ODM_W, BOTH_W, VIS_W
            comp.append([float(row[4]), float(row[5]),
                            float(row[6]), float(row[7])])
            line_count += 1
    print('Processed {0} lines.'.format(line_count))

odometry = np.array(odm)
odmOrigin = odometry[:, 0:3]
# print(odmOrigin.shape)
odmVector = np.array([odometry[:, 0] + np.cos(odometry[:, 2]),
                      odometry[:, 1] + np.sin(odometry[:, 2])]).T
# print(odmVector.shape)

vision = np.array(vis)
visOrigin = vision[:, 0:3]
visVector = np.array([vision[:, 0] + np.cos(vision[:, 2]),
                      vision[:, 1] + np.sin(vision[:, 2])]).T

compare = np.array(comp)
compareOrigin = compare[:, 0:4]


# plt.quiver(odmOrigin[:, 0], odmOrigin[:, 1], odmVector[:, 0], odmVector[:, 1])

############## COMPARE in 2D ################

fig1, (visPlot, odmPlot) = plt.subplots(2)

visPlot.plot(visOrigin[:, 0], visOrigin[:, 1], 'r')

visPlot.set(xlabel='x (m)', ylabel='y (m)',
       title='Vision output points')

odmPlot.plot(odmOrigin[:, 0], odmOrigin[:, 1], 'g')

odmPlot.set(xlabel='x (m)', ylabel='y (m)',
        title='Odometry output points')

fig2, (bothPlot, bothW) = plt.subplots(2)

bothPlot.plot(visOrigin[:, 0], visOrigin[:, 1], 'r')
bothPlot.plot(odmOrigin[:, 0], odmOrigin[:, 1], 'g')
# Square
# bothPlot.plot([-2, 0, 0, -2, -2], [-1, -1, 1, 1, -1], 'black')
# Line
bothPlot.plot([-2, 0.2], [-1, -1], 'black')

# bothPlot.set_xlim([-2.8, -1.5])
# bothPlot.set_ylim([-2, -0.5])

bothPlot.set_xlim([-2.5, 0.5])
bothPlot.set_ylim([-2, 2])

bothPlot.set(xlabel='x (m)', ylabel='y (m)',
             title='Vision and Odometry output points')

bothW.plot(range(len(visOrigin[:, 2])), visOrigin[:, 2], 'r')
bothW.plot(range(len(odmOrigin[:, 2])), odmOrigin[:, 2], 'g')

bothW.set(xlabel='step', ylabel='w (rads)',
          title='Vision and Odometry output angles')

fig1.set_size_inches((8.5, 11), forward=False)
fig2.set_size_inches((8.5, 11), forward=False)
# fig1.savefig("vis-odometry-"+version+".png", dpi=500)
fig2.savefig("vis&odometry-"+version+".png", dpi=500)
# plt.show()


############## COMPARE in 1D ################

# fig3, plot3 = plt.subplots(1)

# plot3.plot(compareOrigin[:, 0], 'black')
# plot3.plot(compareOrigin[:, 1], 'g')
# plot3.plot(compareOrigin[:, 2], 'blue')
# plot3.plot(compareOrigin[:, 3], 'r')

# fig3.set_size_inches((11, 8.5), forward=False)
# fig3.savefig("compare-"+version+".png", dpi=500)
