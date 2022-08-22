# Import libraries
from pickletools import optimize
import matplotlib.pyplot as plt
import os

from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry

class Plotter:  
    def __init__(self, file: Read, org_iJ1, org_wheel_r, new_matrix, final_cost, packet_mod, tsample, limits):
        self.file = file
        self.final_cost = final_cost
        self.odm = Odometry(file, org_iJ1, org_wheel_r, packet_mod, tsample)
        self.optimized_odm = Odometry(file, new_matrix, new_matrix[-1], packet_mod, tsample)
        self.limits = limits

    def get_errors(self):
        simulated = self.odm.simulate_path_angle()
        optimized = self.optimized_odm.simulate_path_angle()
        return self.calculate_error(simulated, optimized)

    def calculate_error(self , simulated, optimized):
        error = Error()
        original_error = error.RMSE(self.file.get_vision_2d(),self.file.get_odometry_2d())
        # print('Original RMSE: {0}'.format(original_error))
        simulated_error = error.RMSE(self.file.get_vision_2d(), simulated[:,0:2])
        # print('Simulated Path RMSE: {0}'.format(simulated_error))
        optimized_error = error.RMSE(self.file.get_vision_2d(), optimized[:,0:2])
        # print('Optimized Path RMSE: {0}'.format(optimized_error))
        return (original_error, simulated_error, optimized_error)

    def plot_vision_odometry_simulated(self, ground_truth="line", limits = (11, 16.5)):
        simulated = self.odm.simulate_path_angle()
        optimized = self.optimized_odm.simulate_path_angle()
        # print("Simulated Path: ", simulated.shape)
        # print("Optimized Path: ", optimized.shape)
        (original_error, simulated_error, optimized_error) = self.calculate_error(simulated, optimized)
        
        figure, (position, angles, errors) = plt.subplots(3)
        position.plot(self.file.get_vision()[:, 0], self.file.get_vision()[:, 1], 'r', label="vision")
        position.plot(self.file.get_odometry()[:, 0], self.file.get_odometry()[:, 1], 'g', label="odometry: RMSE={:.4f}".format(original_error))
        position.plot(simulated[:, 0], simulated[:, 1], 'blue', linestyle='--', label="simulated: RMSE={:.4f}".format(simulated_error))
        position.plot(optimized[:, 0], optimized[:, 1], 'orange', label="optimized: RMSE={:.4f}".format(optimized_error))
        
        position.legend(loc='best')	
        position.set(xlabel='x (m)', ylabel='y (m)', title='Vision, Odometry, Simulated and Optmized positions')
        
        
        if(ground_truth == "square"): # Square
            position.plot([-2, 0, 0, -2, -2], [-1, -1, 1, 1, -1], 'black', label="ground truth", linestyle=':')
            position.set_xlim([-2.8, -1.5])
            position.set_ylim([-2, -0.5])
        elif(ground_truth == "line"): # Line
            position.plot([-2, 0.2], [-1, -1], 'black', label="ground truth", linestyle=':')
            position.set_xlim([-2.5, 0.5])
            position.set_ylim([-1.2, -0.2])


        angles.plot(range(len(self.file.get_vision()[:, 2])), self.file.get_vision()[:, 2], 'r', label="vision")
        angles.plot(range(len(self.file.get_odometry()[:, 2])), self.file.get_odometry()[:, 2], 'g', label="odometry", linestyle=':')
        angles.plot(range(len(simulated[:, 2])), simulated[:, 2], 'blue', label="simulated", linestyle=':')
        angles.plot(range(len(optimized[:, 2])), optimized[:, 2], 'orange', label="optimized", linestyle='--')
        
        angles.legend(loc='best')
        angles.set(xlabel='time steps', ylabel='w (rads)', title='Vision, Odometry and Simulated angles by time step')
        
        errors.bar('odometry to vision', original_error, color='g')
        errors.bar('simulated to vision', simulated_error, color='blue')
        errors.bar('optimized to vision', optimized_error, color='orange')
        errors.bar('combined paths to vision', self.final_cost, color='yellow')
        errors.set(xlabel='comparison', ylabel='errror (RMSE)', title='Odometry, Simulated and Optimized RMSE to Vision')

        figure.set_size_inches(limits, forward=False)
        # print("Analysis from file: {0}".format(self.file.get_path()))
        path = self.get_graph_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)

        figure.savefig(path, dpi=500)
        # plt.show()
    
    def get_file_name(self):
        return self.file.get_path().split('/')[-1]

    def get_result_path(self):
        path = self.file.get_path().replace('data', 'results').split('/')
        path[-1] = "result.json"
        path[-2] = path[-2] + "/limit_" + str(self.limits)
        return "/".join(path)
        
    def get_graph_path(self):
        path = self.file.get_path().replace('data', 'results').split('/')
        path[-2] = path[-2] + "/limit_" + str(self.limits)
        return ("/".join(path)).replace('.csv', '.png')
        

