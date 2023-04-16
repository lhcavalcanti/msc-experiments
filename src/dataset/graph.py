# import modules

# import local libs
from libs.read import Read
from libs.plotter import Plotter

path = 'data/Dataset/mcl_odm_trajectory.csv'
file = Read(path)

if __name__ == '__main__':    
    plotter = Plotter(file, True)
    plotter.plot_vision_odometry(limits =  (5.5, 4.5))
    plotter.plot_vision_mcl(limits =  (5.5, 4.5))
    plotter.plot_vision_odometry_mcl(limits =  (5.5, 4.5))
