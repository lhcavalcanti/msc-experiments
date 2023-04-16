# Import libraries
import matplotlib.pyplot as plt
import os

from libs.read import Read
from libs.error import Error

class Plotter:  
    def __init__(self, file: Read, angle_error=False):
        self.file = file
        self.angle_error = angle_error
        self.error = Error()

    def get_odm_errors(self):
        return self.error.pointDistance(self.file.get_odometry_2d(), self.file.get_vision_2d())
    def get_odm_angle_errors(self):
        return self.error.angular_distances(self.file.get_vision()[:, 2], self.file.get_odometry()[:, 2], True)
    
    def get_mcl_errors(self):
        return self.error.pointDistance(self.file.get_mcl_2d(), self.file.get_vision_2d())
    def get_mcl_angle_errors(self):
        return self.error.angular_distances(self.file.get_vision()[:, 2], self.file.get_mcl()[:, 2], True)


    def plot_vision_odometry(self, limits = (11, 5.5)):
        figure, position = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        position.plot(self.file.get_vision()[:, 0], self.file.get_vision()[:, 1], 'r', label="ground truth")
        position.plot(self.file.get_odometry()[:, 0], self.file.get_odometry()[:, 1], 'g', linestyle='--', label="odometry")
        position.set(xlabel='x (m)', ylabel='y (m)', title='Ground Truth and Odometry positions')
        position.legend(loc='best')	
        path = self.get_graph_path("graphs_split", "odm_path")
        figure.savefig(path, dpi=500)

        figure, angles = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        angles.plot(self.file.get_times(), self.get_odm_angle_errors(), 'g', label="odometry", linestyle='--')
        angles.set(xlabel='time (s)', ylabel='angular difference', title='Angular error from Ground Truth to Odometry on time')
        angles.legend(loc='best')
        path = self.get_graph_path("graphs_split", "odm_angle_error")
        figure.savefig(path, dpi=500)

        figure, angles = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        angles.plot(self.file.get_times(), self.file.get_vision()[:, 2], 'r', label="ground truth")
        angles.plot(self.file.get_times(), self.file.get_odometry()[:, 2], 'g', label="odometry", linestyle='--')
        angles.set(xlabel='time (s)', ylabel='w (degrees)', title='Ground Truth and Odometry angles on time')
        angles.legend(loc='best')
        path = self.get_graph_path("graphs_split", "odm_angles")
        figure.savefig(path, dpi=500)

        figure, errors = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        errors.plot(self.file.get_times(), self.get_odm_errors(), 'g', label="distance")
        errors.set(xlabel='time (s)', ylabel='distance (m)', title='Euclidian distance from Ground Truth to Odometry on time')
        path = self.get_graph_path("graphs_split", "odm_dist_error")
        figure.savefig(path, dpi=500)

        # figure.set_size_inches(limits, forward=False)
        # plt.show()

    def plot_vision_mcl(self, limits = (11, 5.5)):
        figure, position = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        position.plot(self.file.get_vision()[:, 0], self.file.get_vision()[:, 1], 'r', label="ground truth")
        position.plot(self.file.get_mcl()[:, 0], self.file.get_mcl()[:, 1], 'b', linestyle='--', label="MCL")
        position.set(xlabel='x (m)', ylabel='y (m)', title='Ground Truth and MCL positions')
        position.legend(loc='best')
        path = self.get_graph_path("graphs_split", "mcl_positions")
        figure.savefig(path, dpi=500)

        figure, angles = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        angles.plot(self.file.get_times(), self.get_mcl_angle_errors(), 'b', label="MCL", linestyle='--')
        angles.set(xlabel='time (s)', ylabel='angular difference', title='Angular error from Ground Truth to MCL on time')
        angles.legend(loc='best')
        path = self.get_graph_path("graphs_split", "mcl_angle_error")
        figure.savefig(path, dpi=500)
        
        figure, angles = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        angles.plot(self.file.get_times(), self.file.get_vision()[:, 2], 'r', label="ground truth")
        angles.plot(self.file.get_times(), self.file.get_mcl()[:, 2], 'b', label="MCL", linestyle='--')
        angles.set(xlabel='time (s)', ylabel='w (degrees)', title='Ground Truth and MCL angles on time')
        angles.legend(loc='best')
        path = self.get_graph_path("graphs_split", "mcl_angles")
        figure.savefig(path, dpi=500)
        
        figure, errors = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        errors.plot(self.file.get_times(), self.get_mcl_errors(), 'b', label="distance")
        errors.set(xlabel='time', ylabel='distance (m)', title='Euclidian distance from Ground Truth to MCL on time')
        errors.legend(loc='best')
        path = self.get_graph_path("graphs_split", "mcl_dist_error")
        figure.savefig(path, dpi=500)

        # figure.set_size_inches(limits, forward=False)
        # plt.show()

    def plot_vision_odometry_mcl(self, limits = (11, 5.5)):
        figure, position = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        position.plot(self.file.get_vision()[:, 0], self.file.get_vision()[:, 1], 'r', label="ground truth")
        position.plot(self.file.get_odometry()[:, 0], self.file.get_odometry()[:, 1], 'g', linestyle='--', label="odometry")
        position.plot(self.file.get_mcl()[:, 0], self.file.get_mcl()[:, 1], 'b', linestyle='--', label="MCL")
        position.set(xlabel='x (m)', ylabel='y (m)', title='Ground Truth, Odometry and MCL positions')
        position.legend(loc='best')	
        path = self.get_graph_path("graphs_split", "mcl_odm_positions")
        figure.savefig(path, dpi=500)

        figure, angles = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        angles.plot(self.file.get_times(), self.get_odm_angle_errors(), 'g', label="odometry", linestyle='--')
        angles.plot(self.file.get_times(), self.get_mcl_angle_errors(), 'b', label="MCL", linestyle='--')
        angles.set(xlabel='time (s)', ylabel='angular difference', title='Angular error from Ground Truth to Odometry and MCL on time')
        angles.legend(loc='best')
        path = self.get_graph_path("graphs_split", "mcl_odm_angle_error")
        figure.savefig(path, dpi=500)
        

        figure, angles = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        angles.plot(self.file.get_times(), self.file.get_vision()[:, 2], 'r', label="ground truth")
        angles.plot(self.file.get_times(), self.file.get_odometry()[:, 2], 'g', label="odometry", linestyle='--')
        angles.plot(self.file.get_times(), self.file.get_mcl()[:, 2], 'b', label="MCL", linestyle='--')
        angles.set(xlabel='time (s)', ylabel='w (degrees)', title='Ground Truth, Odometry and MCL angles on time')
        angles.legend(loc='best')
        path = self.get_graph_path("graphs_split", "mcl_odm_angles")
        figure.savefig(path, dpi=500)
            
        figure, errors = plt.subplots()
        figure.set_size_inches(limits, forward=False)
        errors.plot(self.file.get_times(), self.get_odm_errors(), 'g', label="odometry distance")
        errors.plot(self.file.get_times(), self.get_mcl_errors(), 'b', label="MCL distance")
        errors.set(xlabel='time', ylabel='distance (m)', title='Distance from Ground Truth to Odometry and to MCL positions on time')
        errors.legend(loc='best')
        path = self.get_graph_path("graphs_split", "mcl_odm_dist_error")
        figure.savefig(path, dpi=500)

        # figure.set_size_inches(limits, forward=False)
        # plt.show()
        
    def get_graph_path(self, graph_type, type = ""):
        path = self.file.get_path().replace('data', 'results').split('/')
        path[-2] = path[-2] + "/" + graph_type
        pathStr = ("/".join(path)).replace('.csv', '_'+type+'.png')
        os.makedirs(os.path.dirname(pathStr), exist_ok=True)
        return pathStr
        

