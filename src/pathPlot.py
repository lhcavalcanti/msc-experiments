# Import libraries
import matplotlib.pyplot as plt
import numpy as np

from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry


version = 'pathing-test5-L-2'
robotFile = 'data/Calibration/21-11-09/Teste 5/test-5-L-logs-2021-11-09.11:56:44.csv'

read = Read(robotFile)
motors = read.getMotors()
vision = read.getVision()
odometry = read.getOdometry()
pcktIds = read.getPacketIds()

## Recreating Path
iJ1 = [[0.34641, 0.282843, -0.282843, -0.34641], [0.414214, -0.414216, -0.414214, 0.414214], [3.616966, 2.556874, 2.556874, 3.616966]]
robotRadius = 0.02475
odm = Odometry(iJ1, robotRadius)
predict = [vision[0].tolist()]
predictIMU = [vision[0].tolist()]
for a in range(len(motors)-1):
    predict.append(odm.newPosition(motors[a], motors[a+1], predict[a], pcktIds[a+1]-pcktIds[a]))
    predictIMU.append(odm.newPositionIMU(motors[a], motors[a+1], predict[a], odometry[a+1,2]-odometry[a,2], pcktIds[a+1]-pcktIds[a]))
predict = np.squeeze(predict)
predictIMU = np.squeeze(predictIMU)


exit
error = Error()

print('Original RMSE: {0}'.format(error.RMSE(read.getVision2D(),read.getOdometry2D())))
print('Predict RMSE: {0}'.format(error.RMSE(read.getVision2D(), predict[:,0:2])))
print('PredictIMU RMSE: {0}'.format(error.RMSE(read.getVision2D(), predictIMU[:,0:2])))


############## TWO in 2D ################

fig1, (visPlot, odmPlot) = plt.subplots(2)

visPlot.plot(read.getVision()[:, 0], read.getVision()[:, 1], 'r')

visPlot.set(xlabel='x (m)', ylabel='y (m)',
       title='Vision output points')

odmPlot.plot(read.getOdometry()[:, 0], read.getOdometry()[:, 1], 'g')

odmPlot.set(xlabel='x (m)', ylabel='y (m)',
        title='Odometry output points')



############### COMPARE in 2D ################

fig2, (bothPlot, bothW) = plt.subplots(2)

bothPlot.plot(read.getVision()[:, 0], read.getVision()[:, 1], 'r')
bothPlot.plot(read.getOdometry()[:, 0], read.getOdometry()[:, 1], 'g')
bothPlot.plot(predict[:, 0], predict[:, 1], 'blue')
bothPlot.plot(predictIMU[:, 0], predictIMU[:, 1], 'yellow')
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
bothW.plot(range(len(predict[:, 2])), predict[:, 2], 'blue')
bothW.plot(range(len(predictIMU[:, 2])), predictIMU[:, 2], 'yellow')

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
