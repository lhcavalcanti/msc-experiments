# Import libraries
import matplotlib.pyplot as plt

from libs.logs import Read
from libs.error import Error

version = 'calibration-test8-S'
robotFile = 'data/Calibration/21-11-09/Teste 8/test-8-S-logs-2021-11-09.12:05:12.csv'

read = Read(robotFile)

# plt.quiver(odmOrigin[:, 0], odmOrigin[:, 1], odmVector[:, 0], odmVector[:, 1])

error = Error()
print('RMSE: {0}'.format(error.RMSE(read.getVision2D(),read.getOdometry2D())))

############## COMPARE in 2D ################

fig1, (visPlot, odmPlot) = plt.subplots(2)

visPlot.plot(read.getVision()[:, 0], read.getVision()[:, 1], 'r')

visPlot.set(xlabel='x (m)', ylabel='y (m)',
       title='Vision output points')

odmPlot.plot(read.getOdometry()[:, 0], read.getOdometry()[:, 1], 'g')

odmPlot.set(xlabel='x (m)', ylabel='y (m)',
        title='Odometry output points')

fig2, (bothPlot, bothW) = plt.subplots(2)

bothPlot.plot(read.getVision()[:, 0], read.getVision()[:, 1], 'r')
bothPlot.plot(read.getOdometry()[:, 0], read.getOdometry()[:, 1], 'g')
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

bothW.plot(range(len(read.getVision()[:, 2])), read.getVision()[:, 2], 'r')
bothW.plot(range(len(read.getOdometry()[:, 2])), read.getOdometry()[:, 2], 'g')

bothW.set(xlabel='step', ylabel='w (rads)',
          title='Vision and Odometry output angles')

fig1.set_size_inches((8.5, 11), forward=False)
fig2.set_size_inches((8.5, 11), forward=False)
# fig1.savefig("vis-odometry-"+version+".png", dpi=500)
fig2.savefig("vis&odometry-"+version+".png", dpi=500)
# plt.show()


############## COMPARE in 1D ################

# fig3, plot3 = plt.subplots(1)

# plot3.plot(read.getCompare()[:, 0], 'black')
# plot3.plot(read.getCompare()[:, 1], 'g')
# plot3.plot(read.getCompare()[:, 2], 'blue')
# plot3.plot(read.getCompare()[:, 3], 'r')

# fig3.set_size_inches((11, 8.5), forward=False)
# fig3.savefig("compare-"+version+".png", dpi=500)
