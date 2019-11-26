import numpy as np
import numpy.random as rand

X_MIN, X_MAX = 0, 1000
Y_MIN, Y_MAX = 0, 1000

MAX_POINTS = 5000
MAX_BOUNDS = 5000

fname = "NONE"

class Node():
    def __init__(self, x: int, y: int, prev):
        self.x = x
        self.y = y
        self.prev = prev

    def as_tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

class RRT():
    def __init__(self, start, goal, bounds, thresh: int):
        start_x = start[0]
        start_y = start[1]

        goal_x = goal[0]
        goal_y = goal[1]

        self.goal = Node(goal_x, goal_y, None)

        self.nodes = [Node(start_x, start_y, None)]

        self.coords = np.zeros((MAX_POINTS, 2))
        self.prev_coords = np.zeros((MAX_POINTS - 1, 2))
        self.bounds = bounds

        self.thresh = thresh

        self.coords[0] = np.array((start_x, start_y))
        self.index = 1

    def add_node(self, x, y):
        prev, dist = self.get_closest_point(x, y)
        x_p, y_p = prev.as_tuple()

        choice_arr = np.array((x, y))
        prev_arr = np.array(prev.as_tuple())
        delta = choice_arr - prev_arr

        delta_len = np.linalg.norm(delta)

        delta *= (self.thresh / delta_len)

        x_n, y_n = (delta + np.array(prev.as_tuple())) if delta_len > self.thresh else (x, y)

        node = Node(x_n, y_n, prev)

        if  self.bounds(node):
            self.nodes.append(node)
            self.coords[self.index] = np.array((x_n, y_n))
            self.prev_coords[self.index - 1] = np.array((x_p, y_p))
            self.index += 1

    def get_closest_point(self, x, y):
        delta_vec = self.coords[ : self.index] - np.tile(np.array((x, y)).reshape(1, 2), (self.index, 1))
        dist_vec = np.sum(delta_vec ** 2, 1)

        cp_index = np.argmin(dist_vec)

        cp = self.nodes[cp_index]
        dist = dist_vec[cp_index]
        return cp, dist

    def within_goal(self, node):
        return (dist(node, self.goal) <= self.thresh) and self.bounds(Node(self.goal.x, self.goal.y, node))

    def next(self):
        x = rand.uniform(X_MIN, X_MAX)
        y = rand.uniform(Y_MIN, Y_MAX)
        self.add_node(x, y)

    def __call__(self):
        while not self.within_goal(self.nodes[self.index - 1]):
            if (self.index >= MAX_POINTS):
                raise ExceededMaxPointsException()
            self.next()
        self.goal.prev = self.nodes[self.index - 1]
        self.nodes.append(self.goal)
        #self.coords[self.index] = self.goal

    def extract_path(self):
        path_coords = np.zeros((self.index, 2, 2))
        node = self.goal
        i = 0
        while node.prev != None:
            entry_tup = (node.prev.as_tuple(), node.as_tuple())
            path_coords[i] = np.array(entry_tup)
            node = node.prev
            i += 1

        path_coords = np.flip(path_coords[ : i], axis=0)
        return path_coords


class Boundaries():
    def __init__(self):
        self.MAX_EDGES = 4 * MAX_BOUNDS
        self.edge_list = np.zeros((self.MAX_EDGES, 3))
        self.bound_list = np.zeros((self.MAX_EDGES, 2))
        self.edge_type = np.zeros((self.MAX_EDGES, 2))
        self.index = 0
        self.dflag = False

    def add_bound(self, p0, p2):

       # p1 = (p2[0], p0[1])
       # p3 = (p0[0], p2[1])

       points = [p0, (p2[0], p0[1]), p2, (p0[0], p2[1])]

       # proj_p0 = convert_to_proj(p0)
       # proj_p1 = convert_to_proj(p1)
       # proj_p2 = convert_to_proj(p2)
       # proj_p3 = convert_to_proj(p3)

       proj_points = [convert_to_proj(p) for p in points]

       # e0 = np.cross(np.array(proj_p0), np.array(proj_p1))
       # e1 = np.cross(np.array(proj_p1), np.array(proj_p2))
       # e2 = np.cross(np.array(proj_p2), np.array(proj_p3))
       # e3 = np.cross(np.array(proj_p3), np.array(proj_p0))

       edges = [np.cross(np.array(proj_points[i % 4]), np.array(proj_points[(i + 1) % 4])) for i in range(4)]  ##CAREFUL OF MAGIC NUMBER

       for i, edge in enumerate(edges):
           self.edge_list[self.index] = edges[i]
           self.bound_list[self.index] = np.array([points[3][i % 2], points[1][i % 2]]) ##CAREFUL OF MAGIC NUMBER
           self.edge_type[self.index] = np.array([(1 - i % 2), (i % 2)])
           self.index += 1

    def check_out_bound(self, node):
        euclid_point = np.array(node.as_tuple())
        euclid_prev_point = np.array(node.prev.as_tuple())

        proj_point = np.array(convert_to_proj(node.as_tuple()))
        proj_prev_point = np.array(convert_to_proj(node.prev.as_tuple()))

        line = np.cross(proj_point, proj_prev_point)

        line_tile = np.tile(line.reshape(1, 3), (self.index, 1))

        intersect = np.cross(self.edge_list[ : self.index], line_tile, 1, 1)
        intersect_euclid = intersect[ : , : 2] / np.tile(intersect[ : , 2].reshape(self.index, 1), (1, 2))

        intersection_coord = intersect_euclid[self.edge_type[ : self.index] != 0]

        orig_point_coord = np.tile(euclid_point.reshape(1, 2), (self.index, 1))[self.edge_type[ : self.index] != 0].reshape(self.index, 1)
        prev_point_coord = np.tile(euclid_prev_point.reshape(1, 2), (self.index, 1))[self.edge_type[ : self.index] != 0].reshape(self.index, 1)

        segment_bounds = np.sort(np.concatenate((orig_point_coord, prev_point_coord), axis=1), axis=1)

        t1 = (intersection_coord > self.bound_list[ : self.index , 0])
        t2 = (intersection_coord < self.bound_list[ : self.index , 1])

        out_bound = ((intersection_coord > segment_bounds[ : , 0]) & (intersection_coord < segment_bounds[ : , 1]) &
                    (intersection_coord > self.bound_list[ : self.index , 0]) & (intersection_coord < self.bound_list[ : self.index , 1]))

        return np.any(out_bound)

    def __call__(self, node):
        return not self.check_out_bound(node)


def convert_to_proj(p):
    return p + (1,)

def dist(n1, n2):
    return ((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2) ** (1/2)

class ExceededMaxPointsException(Exception):
    pass

def debug_bounds(node):
    return (250 < node.x and node.x < 500 and 0 < node.y and node.y < 250)