# import modules
import glob
import json
import pprint
from timeit import repeat
import numpy as np
import multiprocessing as mp
from pyswarms.single.global_best import GlobalBestPSO
from pyswarms.utils.search import GridSearch, RandomSearch

# import local libs
from libs.read import Read
from libs.error import Error
from libs.odometry import Odometry
from libs.plotter import Plotter


orgIJ1 = [[0.34641, 0.282843, -0.282843, -0.34641], [0.414214, -0.414216, -0.414214, 0.414214], [3.616966, 2.556874, 2.556874, 3.616966]]
orgWheelRadius = 0.02475

packet_mod = 255
t_sample = 6.11

# using first 
path = 'data/Calibration/22-11-16-find_params'
files = [Read(i) for i in glob.glob(path+'/*.csv')]


# PSO PARAMETERS
angle_type = "odometry"
num_particles = 20
num_iterations = 40
limit = 0.2

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

    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9} # Original

    options = {'c1': [x*0.1 for x in range(2, 10)] ,
               'c2': [x*0.1 for x in range(2, 10)] ,
               'w' : [x*0.1 for x in range(2, 10)]}

    g = GridSearch(GlobalBestPSO, n_particles=num_particles, dimensions=13,
                   options=options, objective_func=robot_path_error, iters=num_iterations, bounds=bounds)
    
    # options = {'c1': [0.2, 1.2],
    #            'c2': [0.2, 1.2],
    #            'w' : [0.2, 1.2],
    #            'k' : [11, 15],
    #            'p': 1}

    # g = RandomSearch(GlobalBestPSO, n_particles=num_particles, dimensions=13,
    #                options=options, objective_func=robot_path_error, iters=num_iterations, n_selection_iters=10000)
    
    best_score, best_options = g.search()
    
    result = dict()
    result["initial_parameters"] = p.tolist()
    result["initial_simulated_cost"] =  multiples_paths_error(p)
    result["pso_search_options"] = options
    result["pso_iterations"] = num_iterations
    result["pso_n_particles"] = num_particles
    result["pso_limtit"] = limit
    result["pso_best_parameters"] = best_options
    result["best_cost"] = best_score
    
    print("Saving parameters.")
    path = files[0].get_path().replace('data', 'results').split('/')
    path[-1] = "result-"+str(num_particles)+"-limit_" + str(limit) +"-grid-search.json"
    with open("/".join(path), 'w') as f:
        json.dump(result, f, indent=4)



