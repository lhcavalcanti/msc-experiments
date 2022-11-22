# import modules
import os
import json
import multiprocessing as mp
import numpy as np


# import local libs
from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry
from libs.plotter import Plotter


orgIJ1 = [[0.34641, 0.282843, -0.282843, -0.34641], [0.414214, -0.414216, -0.414214, 0.414214], [3.616966, 2.556874, 2.556874, 3.616966]]
orgWheelRadius = 0.02475

packet_mod = 255
t_sample = 5

path = 'data/Calibration/22-11-21'
files = [Read(os.path.join(path, i)) for i in os.listdir(path)]

# 'data/Calibration/22-09-09/logs-2022-09-08-nrf ('+str(i)+').csv' # 8 raw logs with vision navigation
# 'data/Calibration/22-09-12/logs-2022-09-12 ('+str(i)+').csv' # 8 raw logs with optimized vision navigation

def multiples_paths_error(x):
    avg_error = 0
    for file in files:
        avg_error += path_error(x, file)
    return avg_error/len(files)
def path_error(x, file: Read):
     ## Recreating Path
    iJ1 = [[x[0], x[1], x[2], x[3]], [x[4], x[5], x[6], x[7]], [x[8], x[9], x[10], x[11]]]
    robotRadius = x[12]
    odm = Odometry(file, iJ1, robotRadius, packet_mod, t_sample)
    predict = odm.simulate_path_angle()
    error = Error()
    return error.RMSE(file.get_vision_2d(), predict[:,0:2])

def robot_path_error(x):
    pool_obj = mp.Pool()
    errors = pool_obj.map(multiples_paths_error, x)
    return np.array(errors)

if __name__ == '__main__':    
    result = dict()
    print("Generating graphs and result.")
    plotters = [Plotter(file, None, None, None, 0, packet_mod, t_sample, None) for file in files]
    for plotter in plotters:
        plotter.plot_vision_odometry(ground_truth="square")
        (original_error, simulated_error, optimized_error) = plotter.calculate_error()
        result[plotter.get_file_name()] = dict()
        result[plotter.get_file_name()]["odometry_error"] = original_error
    
    print("Saving results.")
    with open(plotter.get_result_path("odometry_vision", "odometry_result"), 'w') as f:
        json.dump(result, f, indent=4)


