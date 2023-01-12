# import modules
import json
import multiprocessing as mp
import numpy as np
import glob




# import local libs
from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry
from libs.plotter import Plotter


orgIJ1 = [[0.34641, 0.282843, -0.282843, -0.34641], [0.414214, -0.414216, -0.414214, 0.414214], [3.616966, 2.556874, 2.556874, 3.616966]]
orgWheelRadius = 0.02475

# Robot 0 first optimization:
# orgIJ1 = [[0.383146590857885, 0.2601908088939393, -0.29432191782356004, -0.2947331116512286], [0.2942690569083855, -0.5298154893258492, -0.4135609185578648, 0.3062489555481053], [3.590359801850708, 2.5770948138832246, 2.572861189728561, 3.6344615627386694]]
# orgWheelRadius = 0.023262252867368625

packet_mod = 255
t_sample = 6.11

path = 'data/Calibration/23-01-11/robot5'
files = [Read(i) for i in glob.glob(path+'/*.csv')]

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
    plotters = [Plotter(file, orgIJ1, orgWheelRadius, None, 0, packet_mod, t_sample, limits=None) for file in files]
    for plotter in plotters:
        plotter.plot_vision_odometry(ground_truth="square", plotSim=False)
        (original_error, simulated_error, optimized_error) = plotter.calculate_error()
        result[plotter.get_file_name()] = dict()
        result[plotter.get_file_name()]["odometry_error"] = original_error
    
    print("Saving results.")
    with open(plotter.get_result_path("odometry_vision", "odometry_result"), 'w') as f:
        json.dump(result, f, indent=4)


