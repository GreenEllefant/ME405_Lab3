"""!
@file main.py
    This file controls two motors to run at the same time. It also sends data to a plotter with data about the motor position.

@author Jack Ellsworth, Hannah Howe, Mathew Smith
@date   13-Feb-2023
@copyright (c) 2023 by Nobody and released under GNU Public License v3
"""

import gc
import pyb
import cotask
import task_share
import utime
from encoder_reader import Encoder_Reader
from position_control import Position_Control
from motor_driver import Motor_Driver
from pyb import UART
pyb.repl_uart(None)

def task1_fun(shares):
    """!
    Runs the motor that is connected tp the A0 and A1 pins.
    @param shares A list holding the queue that contains data to be sent over in task 3
    """
    # Get references to the queue which have been passed to this task
    my_queue = shares

    # Set up encoder for pins C6 and C7
    en1_pin = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    en2_pin = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    timer3 = pyb.Timer(8, prescaler=0, period=0xFFFF)
    e = Encoder_Reader(en1_pin, en2_pin, timer3)
    
    # Set up motor for the B pins
    en_pin = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    in1pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    timer5 = pyb.Timer(5, prescaler = 0, period = 0xFFFF)
    m = Motor_Driver(en_pin, in1pin, in2pin, timer5)
    
    # Set up control class
    Kp = 0.05       # Motor control parameter
    setpoint = 8000 # Move to this position
    c = Position_Control(Kp, setpoint, e, m)
    
    # Pause before running the motor
    yield 0
    start = utime.ticks_ms()
    while True:
        #run for 5 seconds only
        if utime.ticks_ms() - start < 5000:
            c.run(setpoint)
            # Add to the queue for task 3
            serial_string = f"1,{c.values[0]},{c.values[1]}\r\n"
            print(serial_string)
            for one_char in serial_string:
                my_queue.put(ord(one_char))
        else:
            #tell the plotter that we have finished sending data
            serial_string = f"1,-1,0\r\n"
            for one_char in serial_string:
                my_queue.put(ord(one_char))
        yield 0



def task2_fun(shares):
    """!
    Runs the motor that is connected tp the B4 and B5 pins.
    @param shares A list holding the queue that contains data to be sent over in task 3
    """
    # Get references to the queue which have been passed to this task
    my_queue = shares

    # Set up encoder for pins C6 and C7
    en1_pin = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    en2_pin = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer3 = pyb.Timer(4, prescaler=0, period=0xFFFF)
    e1 = Encoder_Reader(en1_pin, en2_pin, timer3)
    
    # Set up motor for the B pins
    en_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    timer5 = pyb.Timer(3, prescaler = 0, period = 0xFFFF)
    m1 = Motor_Driver(en_pin, in1pin, in2pin, timer5)
    
    # Set up control class
    Kp = 0.05       # Motor control parameter
    setpoint = 5000 # Move to this position
    c1 = Position_Control(Kp, setpoint, e1, m1)
    
    # Verify values were added correctly
    print(c1.gain)
    yield 0
    print(c1.setpoint)
    
    
    # Pause before running the motor
    yield 0
    start = utime.ticks_ms()
    while True:
        #Run for 5 seconds only
        if utime.ticks_ms() - start < 5000:
            c1.run(setpoint)
            # Add to the queue for task 3
            serial_string = f"2,{c1.values[0]},{c1.values[1]}\r\n"
            print(serial_string)
            for one_char in serial_string:
                my_queue.put(ord(one_char))
        else:
            #tell the plotter that we have finished sending data
            serial_string = f"2,-1,0\r\n"
            for one_char in serial_string:
                my_queue.put(ord(one_char))
        yield 0

def task3_fun(shares):
    """!
    Sends data in the queue to the plotter
    @param shares A list holding the queue that contains data to be sent to the plotter
    """
    the_queue = shares
    u2 = pyb.UART(2, baudrate=115200)
    while True:
        if the_queue.any():
            data = the_queue.get()
            u2.write(chr(data))
        yield 0

if __name__ == "__main__":
    
    #Wait to start program
    utime.sleep_ms(3000)

    # Create a share and a queue to test function and diagnostic printouts
    q0 = task_share.Queue('B', 200, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks.
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=50,
                         profile=True, trace=False, shares=(q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=50,
                        profile=True, trace=False, shares=(q0))
    #Sending the data needs to run significantly faster so that the queue does not overflow with values.
    task3 = cotask.Task(task3_fun, name="Task_3", priority=3, period=1, profile=True, trace=False, shares=(q0))

    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    # Run the memory garbage collector
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
