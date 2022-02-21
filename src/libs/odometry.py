# Import libraries
from typing import List
import numpy as np
import math

class Odometry:
    iJ1 = np.matrix([[0.34641, 0.282843, -0.282843, -0.34641], 
              [0.414214, -0.414216, -0.414214, 0.414214],
              [3.616966, 2.556874, 2.556874, 3.616966]])
    robotRadius = 0.02475
    matrix = iJ1*robotRadius
    tsample = None
    
    def __init__(self, matrix: list, robotRadius: float, tsample: int = 15):
        self.tsample = tsample
        self.iJ1 = np.reshape(matrix[0:12],(3,4))
        self.robotRadius = robotRadius
        self.matrix = self.iJ1*self.robotRadius

    def updateParameters(self, iJ1: list, robotRadius: float):
        self.iJ1 = np.matrix(iJ1)
        self.robotRadius = robotRadius
        self.matrix = iJ1*robotRadius

    def convertToVector(self, motors: list):
        # print("motors: ", motors)
        return self.matrix * np.matrix(motors).T

    def rotateToGlobal(self, mov: list, w: float):
        iRotate = np.matrix([[math.cos(w), -math.sin(w), 0], [math.sin(w), math.cos(w), 0], [0, 0, 1]])
        # print("Movement: ", mov)
        return iRotate * np.matrix(mov)
    
    def stepMovement(self, pSpeed: list, nSpeed: list):
        # Speed Average
        pSpeed = np.matrix(pSpeed)
        nSpeed = np.matrix(nSpeed)
        speed = pSpeed
        return  self.convertToVector(speed)*(self.tsample/1000)

    def newPosition(self, pSpeed: list, nSpeed: list, pos: list, steps: int):
        movement = steps*self.stepMovement(pSpeed, nSpeed)
        movRotated = self.rotateToGlobal(movement, pos[2])
        return  (np.matrix(pos) + movRotated.T).tolist()[0]
    
    def newPositionIMU(self, pSpeed: list, nSpeed: list, pos: list, angle: float, steps: int):
        movement = steps*self.stepMovement(pSpeed, nSpeed)
        movRotated = self.rotateToGlobal(movement, pos[2])
        movRotated[2] = angle
        return  (np.matrix(pos) + movRotated.T).tolist()[0]
        
