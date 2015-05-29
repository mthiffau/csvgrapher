#!/usr/bin/python

import argparse, sys, time, os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from collections import deque

class RealTimePlot:

    def __init__(self, filename, x_hist, y_range, y_botflex, y_topflex):
        '''Create a real time data plot animation.
        filename:  File to read data from
        x_hist:    How many units of history to show on the graph
        y_range:   Minimum y range values
        y_botflex: Has the user specified that the graph can expand down?
        y_topflex: Has the user specified that the graph can expand up?'''
        self.x_hist = x_hist
        self.y_range = y_range
        self.y_botflex = y_botflex
        self.y_topflex = y_topflex

        self.xvals = deque() # Queue of x values
        self.ysets = []      # Sets of queues of y values
        self.ynames = []     # Names for the y sets plotted

        # Set up the figure as much as we can
        self.fig, self.axis = plt.subplots(num="Real Time Data")
        self.axis.set_ylim(y_range[0], y_range[1])

        # Read as much of the file as has been written so far
        self.filename = filename
        self.fileobj = None
        try:
            self.fileobj = open(filename, 'r')

            # Read all in the file so far
            newdata = self.fileobj.readline()
            while len(newdata) > 0:
                x_val, y_vals = self.parseInput(newdata)
                
                if type(x_val) is str:
                    plt.xlabel(x_val)
                    self.ynames = y_vals
                else:
                    self.addToPlot(x_val, y_vals)
                newdata = self.fileobj.readline()
            
        except Exception as ex:
            print("Exception while trying to open file for reading: " + str(ex))
            self.fileobj = None

        # Plot the data read so far
        self.plotlist = []
        for yset in self.ysets:
            self.plotlist.append(self.xvals)
            self.plotlist.append(yset)
            self.plotlist.append('-')

        if len(self.xvals) > 1:
            self.axis.set_xlim(self.xvals[0], self.xvals[-1])
        self.lines = self.axis.plot(*self.plotlist)

        # Create the legend if we have y labels
        if len(self.ynames) > 0:
            for i in range(len(self.lines)):
                self.lines[i].set_label(self.ynames[i])
            handles, labels = self.axis.get_legend_handles_labels()
            self.axis.legend(handles, labels)
            
        self.anim = animation.FuncAnimation(self.fig, self.update, interval=100)


    def addToPlot(self, x_val, y_vals):
        '''Add a new round of data to the plot. One X value, mutiple Y values.'''
        # Add the x value to the set
        self.xvals.append(x_val)
        # Add the y values to their respective sets
        for i in range(len(y_vals)):
            if len(self.ysets) < (i + 1):
                self.ysets.append(deque())
            self.ysets[i].append(y_vals[i])

        # Purge values if they are too old
        while (x_val - self.xvals[0]) > self.x_hist:
            self.xvals.popleft()
            for yset in self.ysets:
                yset.popleft()
        
        
    def parseInput(self, newdata):
        '''Parse a line of input from the file.'''
        newdata = newdata.rstrip('\n')
        fields = newdata.split(',')
        assert(len(fields) > 1)
        
        if fields[0] == 'names':
            return (fields[1], fields[2:])
        
        x_val = float(fields[0])
        y_vals = list(map(float, fields[1:]))
        
        return (x_val, y_vals)

    
    def update(self, framenum):
        '''Called to update the plot by the animation timer.'''
        if self.fileobj is not None:
            try:
                newdata = self.fileobj.readline()
                if len(newdata) <= 0:
                    return self.lines# If nothing new to read, just return

                # Parse the input
                x_val, y_vals = self.parseInput(newdata)

                # If the inputs are labels, regenerate the legend and return
                if type(x_val) is str:
                    plt.xlabel(x_val)
                    self.ynames = y_vals
                    if len(self.ynames) > 0:
                        for i in range(len(self.lines)):
                            self.lines[i].set_label(self.ynames[i])
                        handles, labels = self.axis.get_legend_handles_labels()
                        self.axis.legend(handles, labels)
                    return self.lines

                # Otherwise add the new data to the plot
                self.addToPlot(x_val, y_vals)

                # Recalculate all the plot axis limits
                miny = self.y_range[0]
                maxy = self.y_range[1]
                
                local_min = 0
                local_max = 0
                
                self.axis.set_xlim(self.xvals[0], self.xvals[-1])
                for i in range(len(self.ysets)):
                    self.lines[i].set_xdata(self.xvals)
                    self.lines[i].set_ydata(self.ysets[i])
                    if self.y_botflex:
                        local_min = min(list(self.ysets[i]))
                        if local_min > 0:
                            miny = min(miny, local_min * 0.9)
                        else:
                            miny = min(miny, local_min * 1.1)
                    if self.y_topflex:
                        local_max = max(list(self.ysets[i]))
                        if local_max > 0:
                            maxy = max(maxy, local_max * 1.1)
                        else:
                            maxy = max(maxy, local_max * 0.9)
                self.axis.set_ylim(miny, maxy)

                # Draw the updated plot
                self.fig.canvas.draw()
                    
            except Exception as ex:
                print("Exception while reading from file: " + str(ex))
                self.fileobj = None

            return self.lines

    def close(self):
        if self.fileobj is not None:
            self.fileobj.close()
            self.fileobj = None
        
if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Real Time CSV Data Grapher")

    parser.add_argument('--xhist', type=float, default=5.0, dest='xhist')
    parser.add_argument('--ylow', type=float, default=-1, dest='ylow')
    parser.add_argument('--yhigh', type=float, default=1, dest='yhigh')
    parser.add_argument('--ytopflex', action='store_true', default=False, dest='ytopflex')
    parser.add_argument('--ybotflex', action='store_true', default=False, dest='ybotflex')
    parser.add_argument('filename', type=str)

    args = parser.parse_args()

    # Create plot
    plot = RealTimePlot(args.filename, args.xhist, (args.ylow, args.yhigh), args.ybotflex, args.ytopflex)

    # Show plot
    plt.show()

