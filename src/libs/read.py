# Import libraries
import csv
import numpy as np

class Read:
    def __init__(self, path, compare = False):
        self.path = path
        self.odometry = []
        self.vision = []
        self.motors = []
        self.pckt_count = []
        self.compare = []
        self.change_state = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # print("Column names are ", ", ".join(row))
                    line_count += 1
                else:
                    self.robotId = row[0]
                    self.odometry.append([float(row[1]), float(row[2]), float(row[3])])
                    self.vision.append([float(row[8]), float(row[9]), float(row[10])])
                    self.pckt_count.append(int(row[14]))
                    self.change_state.append(int(row[15]))
                    if compare:
                        # GYRO_W, ODM_W, BOTH_W, VIS_W
                        self.compare.append([float(row[4]), float(row[5]), float(row[6]), float(row[7])])
                    else:
                        self.motors.append([float(row[4]), float(row[5]), float(row[6]), float(row[7])])
                    line_count += 1
            # print('Processed {0} lines.'.format(line_count))

    def get_odometry(self):
        return np.array(self.odometry)
    
    def get_odometry_2d(self):
        return np.array(self.odometry)[:,0:2]

    def get_odometry_vectors(self):
        odm = self.get_odometry()
        return np.array([odm[:, 0] + np.cos(odm[:, 2]), odm[:, 1] + np.sin(odm[:, 2])]).T

    def get_vision(self):
        return np.array(self.vision)

    def get_vision_2d(self):
        return np.array(self.vision)[:,0:2]

    def get_vision_vectors(self):
        vis = self.get_vision()
        return np.array([vis[:, 0] + np.cos(vis[:, 2]), vis[:, 1] + np.sin(vis[:, 2])]).T

    def get_compare(self):
        if self.compare.Length > 0:
            return np.array(self.compare)

    def get_packet_count(self):
        return np.array(self.pckt_count)
    
    def get_motors(self):
        return np.array(self.motors)

    def get_path(self):
        return self.path

