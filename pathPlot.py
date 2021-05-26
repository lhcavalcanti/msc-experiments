# Import libraries
import math
import csv
import numpy as np
import matplotlib.pyplot as plt

robotFile = 'data/test_1_05-25/robotInfo_clear.csv'

odm = []
vis = []

with open(robotFile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Column names are ", ", ".join(row))
            line_count += 1
        else:
            odm.append([float(row[1]), float(row[2]), float(row[3])])
            vis.append([float(row[4]), float(row[5]), float(row[6])])
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


# plt.quiver(odmOrigin[:, 0], odmOrigin[:, 1], odmVector[:, 0], odmVector[:, 1])


fig, (visPlot, odmPlot) = plt.subplots(2)

visPlot.plot(visOrigin[:, 0], visOrigin[:, 1], 'r')

visPlot.set(xlabel='x (m)', ylabel='y (m)',
       title='Vision output points')

odmPlot.plot(odmOrigin[:, 0], odmOrigin[:, 1], 'g')

odmPlot.set(xlabel='x (m)', ylabel='y (m)',
        title='Odometry output points')

fig2, (bothPlot, bothW) = plt.subplots(2)

bothPlot.plot(visOrigin[:, 0], visOrigin[:, 1], 'r')
bothPlot.plot(odmOrigin[:, 0], odmOrigin[:, 1], 'g')

bothPlot.set(xlabel='x (m)', ylabel='y (m)',
        title='Vision and Odometry output points')

bothW.plot(range(len(visOrigin[:, 2])), visOrigin[:, 2], 'r')
bothW.plot(range(len(odmOrigin[:, 2])), odmOrigin[:, 2], 'g')

bothW.set(xlabel='x (m)', ylabel='y (m)',
        title='Vision and Odometry output angles')


# fig.savefig("test.png")
plt.show()
