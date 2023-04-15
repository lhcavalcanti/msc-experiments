# Import libraries
import csv
import numpy as np

class Read:
    def __init__(self, path):
        self.path = path
        self.odometry = []
        self.mcl = []
        self.vision = []
        self.time = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print("Column names are ", ", ".join(row))
                    line_count += 1
                else:
                    self.mcl.append([float(row[0]), float(row[1]), self.limit_angle(float(row[2]))])
                    self.odometry.append([float(row[3]), float(row[4]), self.limit_angle(float(row[5]))])
                    self.vision.append([float(row[6]), float(row[7]), np.rad2deg(float(row[8]))])
                    self.time.append(float(row[9]))
                    line_count += 1
            print('Processed {0} lines.'.format(line_count))

    def get_odometry(self):
        return np.array(self.odometry)
    
    def get_odometry_2d(self):
        return np.array(self.odometry)[:,0:2]

    def get_odometry_vectors(self):
        odm = self.get_odometry()
        return np.array([odm[:, 0] + np.cos(odm[:, 2]), odm[:, 1] + np.sin(odm[:, 2])]).T
    
    def get_mcl(self):
        return np.array(self.mcl)
    
    def get_mcl_2d(self):
        return np.array(self.mcl)[:,0:2]

    def get_mcl_vectors(self):
        mcl = self.get_mcl()
        return np.array([mcl[:, 0] + np.cos(mcl[:, 2]), mcl[:, 1] + np.sin(mcl[:, 2])]).T

    def get_vision(self):
        return np.array(self.vision)

    def get_vision_2d(self):
        return np.array(self.vision)[:,0:2]

    def get_vision_vectors(self):
        vis = self.get_vision()
        return np.array([vis[:, 0] + np.cos(vis[:, 2]), vis[:, 1] + np.sin(vis[:, 2])]).T

    def get_times(self):
        return np.array(self.time)

    def get_path(self):
        return self.path
    
    def limit_angle(self, angle):
        # reduce the angle  
        angle =  angle % 360
        # force it to be the positive remainder, so that 0 <= angle < 360  
        angle = (angle + 360) % 360
        # force into the minimum absolute value residue class, so that -180 < angle <= 180  
        if (angle > 180):
            angle -= 360
        return angle

