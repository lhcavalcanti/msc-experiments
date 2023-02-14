# import modules
import json
import multiprocessing as mp
import numpy as np
import glob

# import local libs
from libs.read import Read
from libs.error import Error

path = 'data/Calibration/related-works-comparison'

files = [Read(i) for i in glob.glob(path+'/*.csv')]


def max_last_error(file: Read):
    error = Error()
    vision = file.get_vision()
    odometry = file.get_odometry()
    dists = error.pointDistance(vision[:,0:2], odometry[:,0:2])
    print(dists)
    max_dist = 0
    last_dist = 0
    max_angle = 0
    last_angle = 0
    for a in range(len(vision)-1):
        last_dist = dists[a][0]
        if last_dist > max_dist:
            max_dist = last_dist
        last_angle = error.angleDifference(vision[a,2], odometry[a,2])
        if last_angle > max_angle:
            max_angle = last_angle
    return ((max_dist, last_dist), (max_angle, last_angle))


if __name__ == '__main__':    
    result = dict()
    for file in files:
        name = file.get_path().split('/')[-1].split('.')[0]
        print("Processing file: ", name)
        ((max_dist, last_dist), (max_angle, last_angle)) = max_last_error(file)
        result[name] = dict()
        result[name]["max_dist"] = max_dist
        result[name]["last_dist"] = last_dist
        result[name]["max_angle"] = max_angle
        result[name]["last_angle"] = last_angle
        
    print("Saving results.")
    save_path = file.get_path().replace('data', 'results').replace('.csv', '').split('/')
    save_path[-1] = "distance-errors.json"
    save_path = "/".join(save_path)
    print("Saving result.")
    print (result, save_path)
    with open(save_path, 'w') as f:
        json.dump(result, f, indent=4)


