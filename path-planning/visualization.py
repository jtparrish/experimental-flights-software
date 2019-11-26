from matplotlib import collections as mc, patches, pyplot as plt
import numpy as np
from waypoint_rrt import ExceededMaxPointsException

class RRTvis():

    def __init__(self, rrt):
        self.rrt = rrt
        self.index = 0
        plt.ion()


    def plot_all(self):
        try:
            self.rrt()
        except(ExceededMaxPointsException):
            print("RIP")

        bounds = self.rrt.bounds
        
        x = self.rrt.coords[ : self.rrt.index, 0]
        y = self.rrt.coords[ : self.rrt.index, 1]

        line_segs = np.concatenate((self.rrt.prev_coords[ : self.rrt.index - 1].reshape((self.rrt.index - 1), 1, 2), 
            self.rrt.coords[1 : self.rrt.index].reshape((self.rrt.index - 1), 1, 2)), axis=1)
        
        goal_seg = np.array((self.rrt.goal.prev.as_tuple(), self.rrt.goal.as_tuple())).reshape(1, 2, 2)
        line_segs = np.concatenate((line_segs, goal_seg), axis=0)

        fig, ax = plt.subplots()

        rect = patches.Rectangle((250, 0), 250, 250, edgecolor='r', facecolor='none')
        outer_bound = patches.Rectangle((0, 0), 1000, 1000, edgecolor='g', facecolor='none')
        lc = mc.LineCollection(line_segs)

        path = self.rrt.extract_path()

        path_col = mc.LineCollection(path, colors=[(1, 0, 0, 0)]*path.shape[0])

        #ax.add_collection(lc)
        ax.add_collection(path_col)
        ax.add_patch(rect)
        ax.add_patch(outer_bound)

        #ax.plot(x, y)
        plt.scatter(x, y)
        plt.scatter(*self.rrt.goal.as_tuple(), c='r')
        plt.show(block = True)
