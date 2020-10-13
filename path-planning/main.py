import waypoint_rrt as wp
import visualization as visual

def main():
    bounds = wp.Boundaries()
    bounds.add_bound((250,500), (500, 0))
    bounds.add_bound((0, 1000), (500, 550))
    print(bounds.get_points())
    start = (1, 1)
    goal = (999, 999)
    thresh = 100
    rrt = wp.RRT(start, goal, bounds, thresh)
    vis = visual.RRTvis(rrt)
    vis.plot_all()

if __name__ == "__main__":
    main()