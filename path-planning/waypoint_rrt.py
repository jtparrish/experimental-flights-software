import numpy as np

MAX_POINTS = 5000
fname = "NONE"

class Node():
    def __init__(int: x, int: y, Node: prev):
        self.x = x
        self.y = y
        self.prev = prev

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

class Boundaries():
    def __init__():
        pass

class Rectangle():
    def __init__(corner_00, corner_11):
        self.x0 = corner_00[0]
        self.x1 = corner_11[0]
        self.y0 = corner_00[1]
        self.y1 = corner_11[1]
