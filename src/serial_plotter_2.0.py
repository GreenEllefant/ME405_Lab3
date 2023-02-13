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
    tot_list = []
    with serial.Serial('COM5', 115200) as serialPort:
        item = serialPort.readline().split(b',')
        print(item)
        while float(item[1]) != -1.0:
            print(item)
            item = serialPort.readline().split(b',')
            if item[0] == b'1':
                val_list1.append(item)
            else:
                val_list2.append(item)
    
        tot_list.append(val_list1)
        tot_list.append(val_list2)
    return tot_list
            
def plot_me(lists):
    print(lists)
    get_axis = ('Time (in seconds)', 'Position (in encoder ticks)')              #isolate axis titles
    for mot_num in range(len(lists)):
        xpoints =[]
        ypoints =[]
        motor_num = lists[mot_num][0][0]
        for i in range(len(lists[mot_num])-1):
            try:
                xpoints.append(float(lists[mot_num][i][1]))            #add only numerical values to plot list
                ypoints.append(float(lists[mot_num][i][2]))
            except ValueError:
                continue

        pyplot.plot(xpoints, ypoints)           
        pyplot.title("Impulse Response for Motor " + str(int(motor_num)))
        pyplot.xlabel(get_axis[0])
        pyplot.ylabel(get_axis[1])
        pyplot.show()

def main():
    lists = plotter()
    plot_me(lists)
    
if __name__ == "__main__":
    main()