# import modules

# import local libs
from libs.read import Read
from libs.plotter import Plotter

path = 'data/Dataset/mcl_odm_trajectory.csv'
file = Read(path)

if __name__ == '__main__':    
    plotter = Plotter(file, True)
    plotter.plot_vision_odometry()
    plotter.plot_vision_mcl()
    plotter.plot_vision_odometry_mcl()
