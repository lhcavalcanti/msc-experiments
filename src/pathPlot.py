# Import libraries
import matplotlib.pyplot as plt
import numpy as np

from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry


version = 'train-comp-13dim-lim-test5-L-2'
robotFile = 'data/Calibration/21-11-09/Teste 5/test-5-L-logs-2021-11-09.11:56:44.csv'

read = Read(robotFile)
motors = read.getMotors()
vision = read.getVision()
odometry = read.getOdometry()
pckt_ids = read.getPacketIds()

## Original Variables
robotRadius = 0.02475
iJ1 = [[0.34641, 0.282843, -0.282843, -0.34641], [0.414214, -0.414216, -0.414214, 0.414214], [3.616966, 2.556874, 2.556874, 3.616966]]
result_pred = [0.34641, 0.282843, -0.282843, -0.34641, 0.414214, -0.414216, -0.414214, 0.414214, 3.616966, 2.556874, 2.556874, 3.616966, robotRadius]
result_imu = [0.34641, 0.282843, -0.282843, -0.34641, 0.414214, -0.414216, -0.414214, 0.414214, 3.616966, 2.556874, 2.556874, 3.616966, robotRadius]


## Trained  Variables
# result 12 dim
# result_pred = [-0.99481609, -0.28978439,  1.70124942, -1.8630069,   0.7206294,   0.64218566, 1.82867783,  0.41186806, -1.01516988,  0.41604507,  0.6085673,  -1.85021236, robotRadius]
# result 13 dim
# result_pred  = [-1.58833734,  0.77303106,  0.16696222,  1.5808457,   1.17902068,  1.82791228, -2.4033751,   1.00377742,  0.40241043,  1.918566,    2.61539113, -0.38080695, -0.00620572]
# result 13 dim - limiting
# result_pred = [ 0.34198346,  0.27997281, -0.28128674, -0.34427166,  0.41113102, -0.41755156, -0.41047925,  0.41639745,  3.61549701,  2.55385931,  2.5609382, 3.62192546, 0.02285556]
odm = Odometry(result_pred, result_pred[-1])

# result 12 dim (IMU) 
#result_imu = [0.91056241, -1.91661506, -0.49719062, -1.32289257,  1.23435986, -0.40742903, 1.91296489, -0.72801681, -1.56961021,  0.82694107,  0.35211084, -1.65788098, robotRadius]
# result 13 dim  (IMU)
#result_imu = [ 1.62680464,  1.57663445,  2.43047712,  2.59938547,  0.67768298,  2.67908524, 3.7180431,  -0.4371393,  0.84659736,  1.05404983,  2.03679656,  2.40947546, -0.01257848]
# result 13 dim (IMU) - limiting
# result_imu = [ 0.34457893, 0.28331601, -0.28445163, -0.347244, 0.41897556, -0.40955215, -0.41817512, 0.40973083, 3.62083304, 2.55903907, 2.55630442, 3.61569198, 0.02243113]
odm_imu = Odometry(result_imu, result_imu[-1])

predict = [vision[0].tolist()]
predict_imu = [vision[0].tolist()]
for a in range(len(motors)-1):
    predict.append(odm.newPosition(motors[a], motors[a+1], predict[a], pckt_ids[a+1]-pckt_ids[a]))
    predict_imu.append(odm_imu.newPositionIMU(motors[a], motors[a+1], predict_imu[a], odometry[a+1,2]-odometry[a,2], pckt_ids[a+1]-pckt_ids[a]))
predict = np.squeeze(predict)
predict_imu = np.squeeze(predict_imu)


exit
error = Error()

print('Original RMSE: {0}'.format(error.RMSE(read.getVision2D(),read.getOdometry2D())))
print('Predict RMSE: {0}'.format(error.RMSE(read.getVision2D(), predict[:,0:2])))
print('Predict IMU RMSE: {0}'.format(error.RMSE(read.getVision2D(), predict_imu[:,0:2])))


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
bothPlot.plot(predict_imu[:, 0], predict_imu[:, 1], 'yellow')
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
bothW.plot(range(len(predict_imu[:, 2])), predict_imu[:, 2], 'yellow')

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
