# csvgrapher

## grapher.py:
Reads data sequentially out of a file in CSV format and displays it on a graph in real time using Matplotlib.

Required Arguments:

filename - the file you want to read the data from

Optional Arguments:

--xhist FLOAT - How many units of history to display on the graph

--ylow  FLOAT - Default and highest the lower limit of the graph will ever get (can expand down if enabled)

--yhigh FLOAT - Default and lowest the upper limit of the graph will ever get (can expand up if enabled)

--ytopflex    - Allow the graph to expand upwards if there are data values greater than yhigh

--ybotflex    - Allow the graph to expand downwards if there are data values lower than ylow

The script can be stopped with ctrl-c, isn't it fancy?

## datagen.py:
Will generate data with labels into a file called datapipe which can be used to test the grapher. Can also be killed with ctrl-c.

## Data format:
The data in the file should be numbers (integral or floating point) seperated by commas. The first value per line is taken as the X value, and the rest are considered Y values. 

The one special case is if the first item on the line is the string 'names'. If grapher.py sees a line starting with 'names', it will treat the next field as the X label, and the rest as labels for the Y sets being graphed. The labels may be re-emmitted (and therefore changed) at any point.

Ex:
names, time, foo, bar, baz
0.0, 1, 2, 3
0.5, 2, 3, 4
1.0, 3, 4, 5
