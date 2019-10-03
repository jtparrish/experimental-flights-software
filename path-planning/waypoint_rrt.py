import numpy as np
import numpy.random as rand

X_MIN, X_MAX = 0, 1000
Y_MIN, Y_MAX = 0, 1000

MAX_POINTS = 5000
MAX_BOUNDS = 5000

fname = "NONE"

class Node():
    def __init__(int: x, int: y, Node: prev):
        self.x = x
        self.y = y
        self.prev = prev

    def as_tuple(self):
        return (x, y)

class RRT():
    def __init__(int: start_x, int: start_y, Boundaries: bounds, int: thresh):
        self.nodes = [Node(start_x, start_y, None)]
        self.coords = np.zeros((MAX_POINTS, 2))
        self.bounds = bounds

        self.thresh = thresh

        self.coords[0] = np.array((start_x, start_ y))
        self.index = 1

    def add_node(x, y):
        prev, dist = self.get_closest_point(x, y)
        node = Node(x, y, prev)
        if dist <= self.thresh and self.bounds(node):
            nodes.append(node)
            self.coords[i] = np.array((x, y))

    def get_closest_point(x, y):
        delta_vec = self.coords[ : self.index] - np.tile(np.array((x, y)), (self.index, 1))
        dist_vec = np.sum(delta_vec ** 2, 1)

        cp_index = np.argmin(dist_vec)

        cp = self.nodes[cp_index]
        dist = dist_vec[cp_index]
        return cp, dist

    def next(self):
        x = rand.uniform(X_MIN, X_MAX)
        y = rand.uniform(Y_MIN, Y_MAX)


class Boundaries():
    def __init__():
        self.MAX_EDGE = 4 * MAX_BOUND
        self.edge_list = np.zeroes((MAX_EDGE, 3))
        self.bound_list = np.zeroes((MAX_EDGE, 2))
        self.edge_type = np.zeroes((MAX_EDGE, 2))
        self.index = 0

    def add_bound(p0, p2):

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

       edges = [np.cross(np.array(proj_points[i % 4]), np.arry(proj_points[(i + 1) % 4])) for i in range(4)]  ##CAREFUL OF MAGIC NUMBER

       for i, edge in enumerate(edges):
           self.edge_list[self.index] = edges[i]
           self.bound_list[self.index] = np.array([points[3][i % 2], points[1][i % 2]]) ##CAREFUL OF MAGIC NUMBER
           self.edge_type[self.index] = np.array([(1 - i % 2), (i % 2)])
           self.index += 1

    def check_out_bound(node):
        proj_point = convert_to_proj(node.as_tuple())
        proj_prev_point = convert_to_proj(node.prev.as_tuple())

        line = np.cross(np.array(proj_point), np.array(proj_prev_point))

        line_tile = np.tile(line, (self.index, 1))

        intersect = np.cross(self.edge_list[ : self.index], line_tile, 1, 1)
        intersect_euclid = intersect[ : 2] / intersect[2]

        intersection_coord = (intersect_euclid * self.edge_type[ : self.index])[intersection_coord != 0]

        out_bound = (intersection_coord > self.bound_list[ : self.index , 0]) & (intersection_coord < self.bound_list[ : self.index , 1])

        return np.all(out_bound)

    def __call__(self, node):
        return not self.check_out_bound(node)


def convert_to_proj(tuple: p):
    return p + (1,)
