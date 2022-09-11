# import modules
import json
import pprint
from timeit import repeat
import numpy as np
import multiprocessing as mp
from pyswarms.single.global_best import GlobalBestPSO
# from pyswarms.single.local_best import LocalBestPSO

# import local libs
from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry
from libs.plotter import Plotter


orgIJ1 = [[0.34641, 0.282843, -0.282843, -0.34641], [0.414214, -0.414216, -0.414214, 0.414214], [3.616966, 2.556874, 2.556874, 3.616966]]
orgWheelRadius = 0.02475
packet_mod = 255
t_sample = 5
num_files = 8
initial_file = 1
files = [Read('data/Calibration/22-09-09/logs-2022-09-08-nrf ('+str(i)+').csv') for i in range(initial_file, num_files+initial_file)] 

# 'data/Calibration/22-08-10/log_odm_test_L ('+str(i)+').csv'
# 'data/Calibration/22-08-24/logs-2022-08-23 (1).csv'

# 'data/Calibration/22-09-09/logs-2022-09-08-nrf ('+str(i)+').csv' # 8 raw logs with vision navigation

# PSO PARAMETERS
angle_type = "vision"
num_iterations = 10000
limit = 0.16

def multiples_paths_error(x):
    avg_error = 0
    for file in files:
        avg_error += path_error(file, x)
    return avg_error/len(files)
    
def path_error(file: Read, x):
     ## Recreating Path
    iJ1 = [[x[0], x[1], x[2], x[3]], [x[4], x[5], x[6], x[7]], [x[8], x[9], x[10], x[11]]]
    robotRadius = x[12]
    odm = Odometry(file, iJ1, robotRadius, packet_mod, t_sample)
    predict = odm.simulate_path_angle(angle_type)
    error = Error()
    return error.RMSE(file.get_vision_2d(), predict[:,0:2])

def robot_path_error(x):
    pool_obj = mp.Pool()
    errors = pool_obj.map(multiples_paths_error, x)
    return np.array(errors)


if __name__ == '__main__':    
    # instatiate the optimizer
    p = np.append(np.reshape(orgIJ1,(12)), orgWheelRadius)
    p_max = p + limit
    p_min = p - limit
    bounds = (p_min, p_max)
    print("Initial cost: ", multiples_paths_error(p))
    print("Initial parameters: ")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(p)

    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = GlobalBestPSO(n_particles=20, dimensions=13, options=options, bounds=bounds)

    # now run the optimization, pass a=1 and b=100 as a tuple assigned to args
    cost, param = optimizer.optimize(robot_path_error, num_iterations)
    
    result = dict()
    result["initial_parameters"] = p.tolist()
    result["initial_simulated_cost"] =  multiples_paths_error(p)
    result["pso_options"] = options
    result["pso_limtit"] = limit
    result["optimized_parameters"] = param.tolist()
    result["optimized_cost"] = cost
    
    print("Generating graphs and result.")
    plotters = [Plotter(file, orgIJ1, orgWheelRadius, param, cost, packet_mod, t_sample, limit, angle_type) for file in files]
    for plotter in plotters:
        plotter.plot_vision_odometry_simulated_optimized()
        (original_error, simulated_error, optimized_error) = plotter.get_errors()
        result[plotter.get_file_name()] = dict()
        result[plotter.get_file_name()]["odometry_error"] = original_error
        result[plotter.get_file_name()]["simulated_error"] = simulated_error
        result[plotter.get_file_name()]["optimized_error"] = optimized_error

    
    print("Saving parameters.")
    with open(plotter.get_result_path("optimization", "result"), 'w') as f:
        json.dump(result, f, indent=4)



