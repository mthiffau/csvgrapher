# csvgrapher
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

