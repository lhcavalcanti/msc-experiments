# Import libraries
import csv
import numpy as np

class Read:
    odometry = []
    vision = []
    motors = []
    compare = []
    robotId = 0
    def __init__(self, path, compare = False):
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print("Column names are ", ", ".join(row))
                    line_count += 1
                else:
                    self.robotId = row[0]
                    self.odometry.append([float(row[1]), float(row[2]), float(row[3])])
                    self.vision.append([float(row[8]), float(row[9]), float(row[10])])
                    if compare:
                        # GYRO_W, ODM_W, BOTH_W, VIS_W
                        self.compare.append([float(row[4]), float(row[5]), float(row[6]), float(row[7])])
                    else:
                        self.motors.append([float(row[4]), float(row[5]), float(row[6]), float(row[7])])
                    line_count += 1
            print('Processed {0} lines.'.format(line_count))

    def getOdometry(self):
        return np.array(self.odometry)
    
    def getOdometry2D(self):
        return np.array(self.odometry)[:,0:2]

    def getOdometryVectors(self):
        odm = self.getOdometry()
        return np.array([odm[:, 0] + np.cos(odm[:, 2]), odm[:, 1] + np.sin(odm[:, 2])]).T

    def getVision(self):
        return np.array(self.vision)

    def getVision2D(self):
        return np.array(self.vision)[:,0:2]

    def getVisionVectors(self):
        vis = self.getVision()
        return np.array([vis[:, 0] + np.cos(vis[:, 2]), vis[:, 1] + np.sin(vis[:, 2])]).T

    def getCompare(self):
        if self.compare.Length > 0:
            return np.array(self.compare)


