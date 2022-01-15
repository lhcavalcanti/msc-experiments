# Import libraries
import numpy as np

class Kinematics:
    iJ1 = np.matrix([[0.34641, 0.282843, -0.282843, -0.34641], 
              [0.414214, -0.414216, -0.414214, 0.414214],
              [3.616966, 2.556874, 2.556874, 3.616966]])
    robotRadius = 0.02475
    matrix = iJ1*robotRadius
    