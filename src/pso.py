# import modules
import numpy as np
from pyswarms.single.global_best import GlobalBestPSO

# import local libs
from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry

# version = 'pathing-test4-L-1'
dataFile = 'data/Calibration/21-11-09/Teste 5/test-5-L-logs-2021-11-09.11:56:44.csv'

error = Error()
read = Read(dataFile)
motors = read.getMotors()
vision = read.getVision()
odometry = read.getOdometry()
pcktIds = read.getPacketIds()

orgIJ1 = [[0.34641, 0.282843, -0.282843, -0.34641], [0.414214, -0.414216, -0.414214, 0.414214], [3.616966, 2.556874, 2.556874, 3.616966]]
orgRobotRadius = 0.02475
def path_error(x):
     ## Recreating Path
    iJ1 = [[x[0], x[1], x[2], x[3]], [x[4], x[5], x[6], x[7]], [x[8], x[9], x[10], x[11]]]
    robotRadius = x[12]
    odm = Odometry(iJ1, robotRadius)
    # predict = [vision[0].tolist()]
    predictIMU = [vision[0].tolist()]
    for a in range(len(motors)-1):
        # predict.append(odm.newPosition(motors[a], motors[a+1], predict[a], pcktIds[a+1]-pcktIds[a]))
        predictIMU.append(odm.newPositionIMU(motors[a], motors[a+1], predictIMU[a], odometry[a+1,2]-odometry[a,2], pcktIds[a+1]-pcktIds[a]))
    # predict = np.squeeze(predict)
    predictIMU = np.squeeze(predictIMU)

    # return error.RMSE(read.getVision2D(), predict[:,0:2])
    return error.RMSE(read.getVision2D(), predictIMU[:,0:2])

def robot_path_error(x):
    n_particles = x.shape[0]  # number of particles
    errors = [path_error(x[i]) for i in range(n_particles)]
    return np.array(errors)

# instatiate the optimizer
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
p = np.append(np.reshape(orgIJ1,(12)), orgRobotRadius)
p_max = p + 0.005
p_min = p - 0.005
bounds = (p_min, p_max)

optimizer = GlobalBestPSO(n_particles=20, dimensions=13, options=options, bounds=bounds)

# now run the optimization, pass a=1 and b=100 as a tuple assigned to args

cost, pos = optimizer.optimize(robot_path_error, 1000)









# exit


# print('Original RMSE: {0}'.format(error.RMSE(read.getVision2D(),read.getOdometry2D())))
# print('Predict RMSE: {0}'.format(error.RMSE(read.getVision2D(), predict[:,0:2])))
# print('PredictIMU RMSE: {0}'.format(error.RMSE(read.getVision2D(), predictIMU[:,0:2])))