MAX_POINTS =
fname = 

class Node():
    def __init__(int: x, int: y, Node: prev):
        self.x = x
        self.y = y
        self.prev = prev

class RRT():
    def __init__(int: start_x, int: start_y):
        self.points = np.zeros(MAX_POINTS)
