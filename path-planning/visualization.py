from matplotlib import collections as mc, patches, pyplot as plt
import numpy as np
from waypoint_rrt import ExceededMaxPointsException

class RRTvis():
    """
    visualization class for an RRT instance
    """

    def __init__(self, rrt):
        self.rrt = rrt
        self.index = 0
        # enable plotting interactive mode
        plt.ion()


    def plot_all(self):
        """
        handle all plotting
        """
        try:
            # run rrt
            self.rrt()
            # extract the path from the rrt
            path = self.rrt.extract_path()
            # extract the path segment from the last point to the goal
            goal_seg = np.array((self.rrt.goal.prev.as_tuple(), self.rrt.goal.as_tuple())).reshape(1, 2, 2)
        except(ExceededMaxPointsException):
            # rrt failed to generate a path within the maximum number of points
            print("RIP")
            # degenerate RRT path
            path = []
            # empty segment for goal_seg in case of a degenerate RRT
            goal_seg = np.array([], dtype=np.int64).reshape(0, 2, 2)

        bounds = self.rrt.bounds
        
        # extract the x coordinates
        x = self.rrt.coords[ : self.rrt.index, 0]
        # extract the y coordinates
        y = self.rrt.coords[ : self.rrt.index, 1]

        # get the line segments to draw for the tree by concatenating each point in the path to its appropriate previous point
        line_segs = np.concatenate((self.rrt.prev_coords[ : self.rrt.index - 1].reshape((self.rrt.index - 1), 1, 2), 
            self.rrt.coords[1 : self.rrt.index].reshape((self.rrt.index - 1), 1, 2)), axis=1)
        
        # add the segment connecting the goal into the array of segments to draw
        line_segs = np.concatenate((line_segs, goal_seg), axis=0)

        # matplotlib access
        fig, ax = plt.subplots()

        # manually create the patches for the bounds
        ## TODO: MAKE THIS AUTOMATIC
        rect = patches.Rectangle((250, 0), 250, 500, edgecolor='r', facecolor='none')
        h = 450
        rect2 = patches.Rectangle((0, 1000 - h), 500, h, edgecolor='r', facecolor='none')
        # create the rectangle for the outer bound box
        ## TODO: MAKE THIS AUTOMATIC
        outer_bound = patches.Rectangle((0, 0), 1000, 1000, edgecolor='g', facecolor='none')
        # generate a LineCollection object to actually draw the tree segments
        lc = mc.LineCollection(line_segs)

        # write red as rgba value
        red_rgba = (1, 0, 0, 1)

        # generate LineCollection object for drawing the path and
        ## set the path color to red
        path_col = mc.LineCollection(path, colors=[red_rgba])

        # add all of the line segments and rectangle patches to the graph
        ax.add_collection(lc)
        ax.add_collection(path_col)
        ax.add_patch(rect)
        ax.add_patch(rect2)
        ax.add_patch(outer_bound)

        # plot the nodes as actual points
        plt.scatter(x, y)
        # plot the goal node
        plt.scatter(*self.rrt.goal.as_tuple(), c='r')
        # show the plot and block the program
        plt.show(block = True)
