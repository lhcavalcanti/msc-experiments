# import modules
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
trained_parameters = [0.3056409833172562, 0.3363018352994833, -0.23404695106190718, -0.3821316419741716, 0.40398049419707555, -0.3304322345423135, -0.3274095267706663, 0.4201915569973511, 3.6534993885137745, 2.494656148762584, 2.4968297062640725, 3.6986832455144674, 0.025901348179740186]

packet_mod = 255
t_sample = 5
num_files = 2
initial_file = 1
files = [Read('data/Odometry+Vision/09-05-22/log('+str(i)+').csv') for i in range(initial_file, num_files+initial_file)] 

# 'data/Calibration/22-08-10/log_odm_test_L ('+str(i)+').csv'
# 'data/Calibration/22-08-24/logs-2022-08-23 ('+str(i)+').csv'

# 'data/Calibration/22-08-25/odm/logs-2022-08-25 ('+str(i)+').csv'  # 8 Odometry angle test from 22-08-10 data.
# 'data/Calibration/22-08-25/vis/logs-2022-08-25 ('+str(i)+').csv'  # 8 Vision angle test from 22-08-10 data.

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
    # instatiate the optimizer
    result = dict()
    # if len(trained_parameters) == 0:
    #     p = np.append(np.reshape(orgIJ1,(12)), orgWheelRadius)
    #     result["initial_parameters"] = p.tolist()
    # else:
    #     p = trained_parameters
    #     result["initial_parameters"] = p

    # cost =  multiples_paths_error(p)
    # result["initial_simulated_cost"] = cost
    
    print("Generating graphs and result.")
    plotters = [Plotter(file, None, None, None, 0, packet_mod, t_sample, None) for file in files]
    for plotter in plotters:
        plotter.plot_vision_odometry("square")
        (original_error, simulated_error, optimized_error) = plotter.calculate_error()
        result[plotter.get_file_name()] = dict()
        result[plotter.get_file_name()]["odometry_error"] = original_error
    
    print("Saving results.")
    with open(plotter.get_result_path("odometry_vision", "odometry_result"), 'w') as f:
        json.dump(result, f, indent=4)


