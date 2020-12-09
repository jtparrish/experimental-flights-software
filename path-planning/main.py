import waypoint_rrt as wp
import visualization as visual
from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class App:
    def __init__(self, master):
        self.master = master
        # Create a container
        self.frame = Frame(master)

        bounds = wp.Boundaries()
        self.bounds = bounds
        # bounds.add_bound((250, 500), (500, 0))
        # bounds.add_bound((0, 1000), (500, 550))
        # bounds.add_bound((600, 800), (800, 200))
        self.matplot()

        self.frame.pack(side="left")

        self.buttons()


    def matplot(self):

        if not hasattr(self, 'start'):
            self.start = (1, 1)
        if not hasattr(self, 'goal'):
            self.goal = (999, 999)
        thresh = 100
        rrt = wp.RRT(self.start, self.goal, self.bounds, thresh)
        vis = visual.RRTvis(rrt)
        fig = vis.plot_all()

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas.mpl_connect('button_press_event', self.click)
        self.canvas.mpl_connect('motion_notify_event', self.mousemove)

        toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def buttons(self):
        master = Frame(self.master)

        self.bound_buttons(master)

        frame = Frame(master)

        button = Button(master=frame, text="Clear Bounds", command=self.clear_bounds)
        button.pack()

        button = Button(master=frame, text="Refresh", command=self.reload)
        button.pack()

        button = Button(master=frame, text="Quit", command=self.quit)
        button.pack()

        infoText = Label(frame, text="Single click to add bounds.\nDouble left click to set start.\nDouble right click to set goal.")
        infoText.pack()

        frame.pack(side="top")

        master.pack(side="right")

    def bound_buttons(self, master):
        frame = Frame(master)

        title = Label(frame, text="Add Bound", font=(None, 25))
        title.grid(row = 0, columnspan=2)

        topleft_label = Label(frame, text="Top Left Coords")
        topleft_label.grid(row = 2, columnspan=2)

        topleftX_label = Label(frame, text="X: ")
        topleftX_label.grid(row=3, column=0)
        topleftX_entry = Entry(frame)
        topleftX_entry.grid(row=3, column=1)
        self.topleftX_entry = topleftX_entry

        topleftY_label = Label(frame, text="Y: ")
        topleftY_label.grid(row=4, column=0)
        topleftY_entry = Entry(frame)
        topleftY_entry.grid(row=4, column=1)
        self.topleftY_entry = topleftY_entry

        botright_label = Label(frame, text="Bottom Right Coords")
        botright_label.grid(row = 6, columnspan=2)

        botrightX_label = Label(frame, text="X: ")
        botrightX_label.grid(row=7, column=0)
        botrightX_entry = Entry(frame)
        botrightX_entry.grid(row=7, column=1)
        self.botrightX_entry = botrightX_entry

        botrightY_label = Label(frame, text="Y: ")
        botrightY_label.grid(row=8, column=0)
        botrightY_entry = Entry(frame)
        botrightY_entry.grid(row=8, column=1)
        self.botrightY_entry = botrightY_entry

        button = Button(master=frame, text="Add", command=self.bound_button)
        button.grid(row=10, columnspan=2)
        
        frame.pack(side="top")

    def bound_button(self):
        topleftX = self.topleftX_entry.get()
        topleftY = self.topleftY_entry.get()
        botrightX = self.botrightX_entry.get()
        botrightY = self.botrightY_entry.get()
        topleftX = int(topleftX)
        topleftY = int(topleftY)
        botrightX = int(botrightX)
        botrightY = int(botrightY)
        self.bounds.add_bound((topleftX, topleftY), (botrightX, botrightY))
        self.reload()

    def clear_bounds(self):
        self.bounds = wp.Boundaries()
        self.reload()

    def reload(self):
        for child in self.frame.winfo_children():
            child.destroy()
        self.matplot()

    def quit(self):
        self.master.quit()
        self.master.destroy()

    def click(self, event):
        ix, iy = float(event.xdata), float(event.ydata)
        if(event.dblclick):
            if(event.button == 1):
                self.start = (ix, iy)
            elif(event.button == 3):
                self.goal = (ix, iy)
            if hasattr(self, 'boundstart'):
                del self.boundstart
            self.reload()
        else:
            if hasattr(self, 'boundstart'):
                self.bounds.add_bound((min(ix, self.boundstart[0]), max(iy, self.boundstart[1])), (max(ix, self.boundstart[0]), min(iy, self.boundstart[1])))
                del self.boundstart
                self.reload()
            else :
                self.boundstart = (ix, iy)
        

    def mousemove(self, event):
        # print("here")
        2+2


def main():
    window = Tk()
    app = App(window)
    window.mainloop()

if __name__ == "__main__":
    main()
