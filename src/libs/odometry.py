# Import libraries
from typing import List
import numpy as np
import math

# iJ1 = np.matrix([[0.34641, 0.282843, -0.282843, -0.34641], 
#             [0.414214, -0.414216, -0.414214, 0.414214],
#             [3.616966, 2.556874, 2.556874, 3.616966]])
# robotRadius = 0.02475
class Odometry:
    def __init__(self, file, matrix: list, robotRadius: float, mod = None, tsample: int = 15):
        self.tsample = tsample
        self.iJ1 = np.reshape(matrix[0:12],(3,4))
        self.robotRadius = robotRadius
        self.matrix = self.iJ1*self.robotRadius
        self.file = file;
        self.mod = mod

    def simulate_path(self):
        vision = self.file.get_vision()
        motors = self.file.get_motors()
        pckt_cnt = self.file.get_packet_count()
        path_simulation = [vision[0].tolist()]
        for a in range(len(motors)-1):
            packet_diff = pckt_cnt[a+1]-pckt_cnt[a]
            if self.mod != None:
                packet_diff = packet_diff % self.mod
            path_simulation.append(self.new_position(motors[a], motors[a+1], path_simulation[a], packet_diff))
        path_simulation = np.squeeze(path_simulation)
        return path_simulation

    def simulate_path_angle(self):
        vision = self.file.get_vision()
        motors = self.file.get_motors()
        odometry = self.file.get_odometry()
        pckt_cnt = self.file.get_packet_count()
        path_simulation = [vision[0].tolist()]
        for a in range(len(motors)-1):
            angle_diff = odometry[a+1,2]-odometry[a,2]
            packet_diff = pckt_cnt[a+1]-pckt_cnt[a]
            if self.mod != None:
                packet_diff = packet_diff % self.mod
            path_simulation.append(self.new_position_angle(motors[a], motors[a+1], path_simulation[a], angle_diff, packet_diff))
        path_simulation = np.squeeze(path_simulation)
        return path_simulation

    def update_parameters(self, iJ1: list, robotRadius: float):
        self.iJ1 = np.reshape(iJ1[0:12],(3,4))
        self.robotRadius = robotRadius
        self.matrix = iJ1*robotRadius

    def convert_to_vector(self, motors: list):
        # print("motors: ", motors)
        return self.matrix * np.matrix(motors).T

    def rotate_to_global(self, mov: list, w: float):
        iRotate = np.matrix([[math.cos(w), -math.sin(w), 0], [math.sin(w), math.cos(w), 0], [0, 0, 1]])
        # print("Movement: ", mov)
        return iRotate * np.matrix(mov)
    
    def step_movement(self, prev_speed: list, next_speed: list):
        # Speed Average
        prev_speed = np.matrix(prev_speed)
        next_speed = np.matrix(next_speed)
        speed = prev_speed
        return  self.convert_to_vector(speed)*(self.tsample/1000)

    def new_position(self, prev_speed: list, next_speed: list, pos: list, steps: int):
        movement = steps*self.step_movement(prev_speed, next_speed)
        movRotated = self.rotate_to_global(movement, pos[2])
        return  (np.matrix(pos) + movRotated.T).tolist()[0]
    
    def new_position_angle(self, prev_speed: list, next_speed: list, pos: list, angle: float, steps: int):
        movement = steps*self.step_movement(prev_speed, next_speed)
        movRotated = self.rotate_to_global(movement, pos[2])
        movRotated[2] = angle
        return  (np.matrix(pos) + movRotated.T).tolist()[0]
    
    def get_parameters(self):
        return (self.iJ1, self.robotRadius)
        
