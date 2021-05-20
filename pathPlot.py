# Import libraries
import math
import csv
import numpy as np
import matplotlib.pyplot as plt

odmX = []
odmY = []
odmW = []
odm = []
pos = []

with open('robotOdm_clear.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Column names are ", ", ".join(row))
            line_count += 1
        else:
            odmX.append(float(row[1]))
            odmY.append(float(row[2]))
            w = float(row[3])
            # if w < 0:
            #     w = w+2*math.pi
            odmW.append(w)
            odm.append([float(row[1]), float(row[2]), w])
            line_count += 1
    print('Processed {0} lines.'.format(line_count))

with open('robotPos_clear.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Column names are ", ", ".join(row))
            line_count += 1
        else:
            w = float(row[3])
            # if w < 0:
            #     w = w+2*math.pi
            pos.append([float(row[1]), float(row[2]), w])
            line_count += 1
    print('Processed {0} lines.'.format(line_count))


odometry = np.array(odm)
odmOrigin = odometry[:, 0:2]
# print(odmOrigin.shape)
odmVector = np.array([odometry[:, 0] + np.cos(odometry[:, 2]),
                      odometry[:, 1] + np.sin(odometry[:, 2])]).T
# print(odmVector.shape)

vision = np.array(pos)
visOrigin = vision[:, 0:2]
visVector = np.array([vision[:, 0] + np.cos(vision[:, 2]),
                      vision[:, 1] + np.sin(vision[:, 2])]).T


# plt.quiver(odmOrigin[:, 0], odmOrigin[:, 1], odmVector[:, 0], odmVector[:, 1])


fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(visOrigin[:, 0], visOrigin[:, 1])

ax1.set(xlabel='x (m)', ylabel='y (m)',
       title='Vision output points')

ax2.plot(odmOrigin[:, 0], odmOrigin[:, 1])

ax2.set(xlabel='x (m)', ylabel='y (m)',
        title='Odometry output points')

fig2, ax = plt.subplots()

ax.plot(visOrigin[:, 0], visOrigin[:, 1], 'r')
ax.plot(odmOrigin[:, 0], odmOrigin[:, 1], 'g')

ax.set(xlabel='x (m)', ylabel='y (m)',
        title='Vision and Odometry output points')


# fig.savefig("test.png")
plt.show()
