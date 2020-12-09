from matplotlib import collections as mc, patches, pyplot as plt
import numpy as np
from waypoint_rrt import ExceededMaxPointsException
from PIL import Image

class RRTvis():
    """
    visualization class for an RRT instance
    """

    def __init__(self, rrt):
        self.rrt = rrt
        self.index = 0
        # enable plotting interactive mode THIS BREAKS UI, DONT UNCOMMENT
        # plt.ion()


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

        #displays gatech map as background
        im = np.array(Image.open('gatech-map.jpg'), dtype=np.uint8)
        ax.imshow(im)

        # create the patches for the bounds that user has inputted
        rects = []
        for coords in bounds.get_points():
            xcoord = coords[0][0]
            ycoord = coords[1][1]
            width = coords[1][0] - coords[0][0]
            height = coords[0][1] - coords[1][1]
            rects.append(patches.Rectangle((xcoord, ycoord), width, height, edgecolor='r', facecolor='none'))

        ## TODO: MAKE THIS AUTOMATIC
        # creates patches for the outer bounds
        outer_bound = patches.Rectangle((0, 0), 1325, 1050, edgecolor='g', facecolor='none')
        # generate a LineCollection object to actually draw the tree segments
        lc = mc.LineCollection(line_segs)

        # write blue as rgba value
        blue = (0, 0, 1, 1)

        # generate LineCollection object for drawing the path and
        ## set the path color to red
        path_col = mc.LineCollection(path, colors=[blue])

        # add all of the line segments and rectangle patches to the graph
        for r in rects:
            ax.add_patch(r)
        # ax.add_collection(lc)
        ax.add_collection(path_col)
        ax.add_patch(outer_bound)

        # plot the nodes as actual points
        # plt.scatter(x, y)
        # plot the goal node
        plt.scatter(*self.rrt.goal.as_tuple(), c='r')
        # return figure so main method can display it
        return fig
