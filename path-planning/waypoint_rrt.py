import numpy as np
import numpy.random as rand

# bounds for the overall arena
X_MIN, X_MAX = 0, 1000
Y_MIN, Y_MAX = 0, 1000

# maximum number of points
MAX_POINTS = 5000
# maximum number of boundary regions
MAX_BOUNDS = 5000

fname = "NONE"

# class to store a tree node
## stores its coordinates as well as a reference to the previous node
class Node():
    def __init__(self, x: int, y: int, prev):
        self.x = x
        self.y = y
        self.prev = prev

    def as_tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

# rrt class
class RRT():
    def __init__(self, start, goal, bounds, thresh: int):
        """
        + start is the start point of the path planning in the form (start_x, start_y)
        + goal is the goal point of the path planning in the form (goal_x, goal_y)
        + bounds is a bounds object for the arena
        + thresh is the threshold for within which a point will be attached
        """
        start_x = start[0]
        start_y = start[1]

        goal_x = goal[0]
        goal_y = goal[1]

        self.goal = Node(goal_x, goal_y, None)

        # save list of node objects
        self.nodes = [Node(start_x, start_y, None)]

        self.coords = np.zeros((MAX_POINTS, 2))
        self.prev_coords = np.zeros((MAX_POINTS - 1, 2))
        self.bounds = bounds

        self.thresh = thresh

        self.coords[0] = np.array((start_x, start_y))
        self.index = 1

    def add_node(self, x, y):
        """
        attempt to add the point (x,y) to the rrt or its projection if it is beyond the threshold;
        do nothing if this fails
        """
        # get the closest point and the distance to that point
        prev, dist = self.get_closest_point(x, y)

        # extract previous x and y
        x_p, y_p = prev.as_tuple()

        # construct the random point (x,y) as a numpy array
        choice_arr = np.array((x, y))
        # construct the previous point as a numpy_array
        prev_arr = np.array(prev.as_tuple())
        # get the displacement vector as a numpy array
        delta = choice_arr - prev_arr

        # get the magnitude of the distance vector
        delta_len = np.linalg.norm(delta)

        # scale the distance vector back to be exactly thresh units in length
        delta *= (self.thresh / delta_len)

        # select the point at the scaled distance vector if the original point was outside the threshold
        ## o.w. select the original point
        x_n, y_n = (delta + np.array(prev.as_tuple())) if delta_len > self.thresh else (x, y)

        # construct a node object holding the new point and connecting to the previous point
        node = Node(x_n, y_n, prev)

        # check that the new edge (prev.x, prev.y) <-> (x_n, y_n) does not cross any boundary boxes
        if self.bounds(node):
            # append the node to the list of nodes
            self.nodes.append(node)
            # place the coordinates of the new point in the coordinate array
            self.coords[self.index] = np.array((x_n, y_n))
            # place the coordinates of the new points ancestor in the prev array
            self.prev_coords[self.index - 1] = np.array((x_p, y_p))
            #increment the counter/index
            self.index += 1

    def get_closest_point(self, x, y):
        """
        find's the closest point already in the tree to the point (x, y)
        -> returns the closest point and the distance to that point in the form (point, distance)
        """
        # compute the displacement vectors between each point in the tree and the new point in parallel
        delta_vec = self.coords[ : self.index] - np.tile(np.array((x, y)).reshape(1, 2), (self.index, 1))

        # compute the distance from each point to the new point in parallel
        dist_vec = np.sum(delta_vec ** 2, 1) ** .5

        # get the index of the closest point
        cp_index = np.argmin(dist_vec)

        # get the closest point and the distance to that point
        cp = self.nodes[cp_index]
        dist = dist_vec[cp_index]
        return cp, dist

    # determine if a point is within range of the goal and can be connected without crossing a boundary area
    def within_goal(self, node):
        return (dist(node, self.goal) <= self.thresh) and self.bounds(Node(self.goal.x, self.goal.y, node))

    # generate new point and attempt to add it to the rrt
    def next(self):
        x = rand.uniform(X_MIN, X_MAX)
        y = rand.uniform(Y_MIN, Y_MAX)
        self.add_node(x, y)

    # run the rrt
    def __call__(self):
        # if we are within reach of the goal, go there directly; o.w. keep adding points to the tree
        while not self.within_goal(self.nodes[self.index - 1]):
            if (self.index >= MAX_POINTS):
                # too many points have been added and no path has been found
                raise ExceededMaxPointsException()
            # attempt to add a new point to the rrt
            self.next()
        # set the previous node of the goal to be the last node added
        self.goal.prev = self.nodes[self.index - 1]
        self.nodes.append(self.goal)
        #self.coords[self.index] = self.goal

    def extract_path(self):
        """
        extracts the path to the goal from the solved RRT in the form of an array of line segments
        """
        # initialize the path coordinates array
        ## path_coords[i][0] = previous coordinates
        ## path_coords[i][1] = current coordinates
        path_coords = np.zeros((self.index, 2, 2))
        # initialize node to the goal
        node = self.goal
        # initialize the index
        i = 0
        while node.prev != None:
            # generate a tuple of the form ((prev.x, prev.y), (curr.x, curr.y))
            entry_tup = (node.prev.as_tuple(), node.as_tuple())
            # enter the previous and current coordinates into the path array
            path_coords[i] = np.array(entry_tup)
            # move to the previous node
            node = node.prev
            # increment index
            i += 1

        # flip the coordinates so that the first segment is (start, x) and the last is (y goal)
        path_coords = np.flip(path_coords[ : i], axis=0)
        # smooth the path before returning it
        return self.smooth(path_coords)

    def smooth(self, path):
        """
        takes an RRT path an attempts to smooth it by using a heuristic that ammounts to
        "travel as far as you can along the path each step". This helps cut out the jaggedness,
        particularly when the path runs through open space. If there are no obstacles in the way,
        this smoother will result in a direct path to the goal. Otherwise the path it returns
        is likely suboptimal, but typically much better than the raw path.
        """

        # generate the new path
        new_path = np.zeros(path.shape)
        # save the number of points in the original path
        N = path.shape[0]

        # the index for the modified path
        i_prime = 0
        # the index for the original path
        i = 0

        # print(N)

        # loop until we have connected the goal (i = N-1)
        while i < N - 1:
            # initialize the previous node to the current node indicated by i
            prev_node = Node(path[i][0][0], path[i][0][1], None)
            # iterate backwards from the goal attempting a connection
            for j in reversed(range(i, N)):
                # get the node at destination node of segment j and set the origin of segment i as its previous
                ## thus we are attmepting to skip segments i through j and replace them with a direct connection
                node = Node(path[j][1][0], path[j][1][1], prev_node)
                # check if the two nodes can be directly connected
                if self.bounds(node):
                    # set the previous node for this leg in the new path
                    new_path[i_prime][0] = path[i][0]
                    # set the destination node for this leg in the new path
                    new_path[i_prime][1] = path[j][1]
                    # increment to set the next leg in the new path
                    i_prime += 1
                    # increment the start of the next segment to the segment originating at the destination of the segment
                    ## just added to the new path
                    i = j+1
                    # break out of the for loop
                    break

        # print(new_path[ : i_prime])

        # return the new path which is only valid up to i_prime
        ## (the rest was not used)
        return new_path[ : i_prime]


                

# class representing a collection of rectangular boundary regions in the arena
class Boundaries():
    def __init__(self):
        self.point_list = np.zeros((MAX_BOUNDS, 2, 2))
        # set the maximum number of edges
        self.MAX_EDGES = 4 * MAX_BOUNDS
        # generate an array of edge lines in projective representation
        self.edge_list = np.zeros((self.MAX_EDGES, 3))
        # generate an array of bounding values for each of the edges
        ## (edges will be vertical or horizontal so we only need one number for each bound)
        self.bound_list = np.zeros((self.MAX_EDGES, 2))
        # generate an array storing the type of edge
        ## edge_type[i] = [1, 0] if the edge_list[i] is vertical o.w. the edge is horizontal and edge_type[i] = [0, 1]
        self.edge_type = np.zeros((self.MAX_EDGES, 2))
        # initialize the edge index
        self.index = 0

    def add_bound(self, p0, p2):
        """
        add the given rectangle to the bounds stored in this object
        + p0 the bottom left corner of the rectangle
        + p2 the upper right corner of the rectangle
        """

        self.point_list[self.index // 4] = [p0, p2]

        # get the four corners of the rectangle
        points = [p0, (p2[0], p0[1]), p2, (p0[0], p2[1])]

        # get the four corners of the rectangle in projective form
        proj_points = [convert_to_proj(p) for p in points]

        # get the four edges in projective coordinates
        edges = [np.cross(np.array(proj_points[i % 4]), np.array(proj_points[(i + 1) % 4])) for i in range(4)]  ##CAREFUL OF MAGIC NUMBER

        # add the edges to the various registration lists
        for i, edge in enumerate(edges):
            # add the edge itself to the edge list
            self.edge_list[self.index] = edges[i]
            # add the bounds (endpoints) of the edge to the bound list
            self.bound_list[self.index] = np.array([points[3][i % 2], points[1][i % 2]]) ##CAREFUL OF MAGIC NUMBER
            # set the edge type in the edge type list
            self.edge_type[self.index] = np.array([(1 - i % 2), (i % 2)])
            # increment the index for the next edge
            self.index += 1

    def get_points(self):
        """
        return the array of corner points for the rectangles in the boundary object
        
        each element of the array represents a rectangle and has the form
        [
            [upper_left.x, upper_left.y],
            [lower_right.x, lower_riht.y]
        ]
        """
        return self.point_list[ : self.index // 4]

    def check_out_bound(self, node):
        """
        check if the path between the given node and the nodes previous node goes through any of the bounding boxes
        """
        
        # get the node as an np array of cartesian coordinates
        cart_point = np.array(node.as_tuple())
        # get the previous node as an np array of cartesian coordinates
        cart_point = np.array(node.prev.as_tuple())

        # get the node as an np array of projective coordinates
        proj_point = np.array(convert_to_proj(node.as_tuple()))
        # get the previous node as an np array of projective coordinates
        proj_prev_point = np.array(convert_to_proj(node.prev.as_tuple()))

        # get the projective representation of the line between the two points
        line = np.cross(proj_point, proj_prev_point)

        # tile the line for SIMD computation with each edge 
        line_tile = np.tile(line.reshape(1, 3), (self.index, 1))

        # compute the intersection between the line between the two points and each edge in projective coordinates 
        intersect = np.cross(self.edge_list[ : self.index], line_tile, 1, 1)
        # convert to euclidean intersection
        intersect_euclid = intersect[ : , : 2] / np.tile(intersect[ : , 2].reshape(self.index, 1), (1, 2))

        # extract the pertinent intersection coordinate for each edge (x for hotizontal edges, y for vertical edges)
        intersection_coord = intersect_euclid[self.edge_type[ : self.index] != 0]

        # 
        orig_point_coord = np.tile(cart_point.reshape(1, 2), (self.index, 1))[self.edge_type[ : self.index] != 0].reshape(self.index, 1)
        prev_point_coord = np.tile(cart_point.reshape(1, 2), (self.index, 1))[self.edge_type[ : self.index] != 0].reshape(self.index, 1)

        segment_bounds = np.sort(np.concatenate((orig_point_coord, prev_point_coord), axis=1), axis=1)

        t1 = (intersection_coord > self.bound_list[ : self.index , 0])
        t2 = (intersection_coord < self.bound_list[ : self.index , 1])

        out_bound = ((intersection_coord > segment_bounds[ : , 0])
                    & (intersection_coord < segment_bounds[ : , 1])
                    & (intersection_coord > self.bound_list[ : self.index , 0])
                    & (intersection_coord < self.bound_list[ : self.index , 1]))

        return np.any(out_bound)

    def __call__(self, node):
        return not self.check_out_bound(node)

def convert_to_proj(p):
    """
    helper function to convert a cartesian point p (passed as a tuple (x, y)) into
    an equivalent point in homogenous coordinates (a tuple (x, y, 1))
    """
    return p + (1,)

def dist(n1, n2):
    """
    return the euclidean distance between two euclidean points (represented as node objects)
    """
    return ((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2) ** (1/2)

class ExceededMaxPointsException(Exception):
    """
    exception class signaling that the RRT process exceeded the maximum number of exploratory points specified
    and failed to connect the origin to the goal
    """
    pass

# def debug_bounds(node):
#     return (250 < node.x and node.x < 500 and 0 < node.y and node.y < 250)