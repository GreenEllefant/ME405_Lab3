"""! @Serial_plotter.py
    This file waits for the board to send data through the computer's COM5 serial port.
    Utilizes the Python PC compiler
    @author Jack Ellsworth, Hannah Howe, Mathew Smith
    @date   5-Feb-2023
    @copyright (c) 2023 by Nobody and released under GNU Public License v3
"""

import serial
from matplotlib import pyplot

"""!
@details: 
uses serial port to take in position and time data as 2D byte array
will return a plot of the points, number of points determined by response sent via UART
first two values read are length of data set and chosen gain respectively
"""

def plotter():
    val_list1 = []
    val_list2 = []                                       
    with serial.Serial('COM5', 115200, timeout=5) as serialPort:
        item = serialPort.readline().split(b',')
        while float(item[1]) != -1.0:
            item = serialPort.readline().split(b',')
            if item[0] == 1:
                val_list1.append(item)
            else:
                val_list2.append(item)
    yield val_list1, val_list2
            
def plot_me(lists):
    get_axis = ('Time (in seconds)', 'Position (in encoder ticks)')              #isolate axis titles
    for mot_num in range(1, 2):
        xpoints =[]
        ypoints =[]
        motor_num = list[mot_num][0]
        for i in range(len(list[mot_num])-1):
            try:
                xpoints.append(float(list[mot_num][i][0]))            #add only numerical values to plot list
                ypoints.append(float(list[mot_num][i][1]))
            except ValueError:
                continue

        pyplot.plot(xpoints, ypoints)           
        pyplot.title("Impulse Response for Motor ", motor_num)
        pyplot.xlabel(get_axis[0])
        pyplot.ylabel(get_axis[1])
        pyplot.show()

def main():
    lists = plotter()
    plot_me(lists)
    
if name == "__main__":
    main()