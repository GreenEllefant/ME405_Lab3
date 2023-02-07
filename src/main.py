"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
from encoder_reader import Encoder_Reader
from position_control import Position_Control
from motor_driver import Motor_Driver


def task1_motor1(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_queue = shares

    # Set up encoder for pins C6 and C7
    en1_pin = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    en2_pin = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    timer3 = pyb.Timer(3, prescaler=0, period=0xFFFF)
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
    
    while True:
        c.run(setpoint)
        # Add to the queue for task 3
        serial_string = f"1,{c.values[0]},{c.values[1]}\r\n"
        print(serial_string)
        for one_char in serial_string.encode():
            my_queue.put(one_char)
        yield 0

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a queue to test function and diagnostic printouts
    q0 = task_share.Queue('B', 1000, thread_protect=False, overwrite=False,
                          name="Serial Queue")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_motor1, name="Task_1: Motor 1", priority=1, period=10,
                        profile=True, trace=False, shares=(q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=1500,
                        profile=True, trace=False, shares=(q0))
    cotask.task_list.append(task1)
    #cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
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
