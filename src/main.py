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
import utime
from pyb import UART
pyb.repl_uart(None)

def task1_fun(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_queue = shares
    i = 0
    counter = 0
    while True:
        dummy_data=[[1,10,0],
                    [1,20,50],
                    [1,30,150],
                    [1,40,200],
                    [1,50,-50],
                    [1,-1,50]]
        if i < len(dummy_data):
            data = f"{dummy_data[i][0]},{dummy_data[i][1]},{dummy_data[i][2]}\r\n"
            for char in data:
                my_queue.put(ord(char))
            i += 1
        yield 0


def task2_fun(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    my_queue = shares
    i = 0
    while True:
        # Show everything currently in the queue and the value in the share
        dummy_data =   [[2,10,0],
                        [2,20,-50],
                        [2,30,-150],
                        [2,40,-200],
                        [2,50,50],
                        [2,-1,50]]
        if i < len(dummy_data):
            data = f"{dummy_data[i][0]},{dummy_data[i][1]},{dummy_data[i][2]}\r\n"
            for char in data:
                my_queue.put(ord(char))
            i += 1
        yield 0

def task3_fun(shares):
    the_queue = shares
    u2 = pyb.UART(2, baudrate=115200)
    while True:
        if the_queue.any():
            data = the_queue.get()
            u2.write(chr(data))
        yield 0

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")
    
    utime.sleep_ms(3000)

    # Create a share and a queue to test function and diagnostic printouts
    q0 = task_share.Queue('B', 200, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=150,
                        profile=True, trace=False, shares=(q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=150,
                        profile=True, trace=False, shares=(q0))
    task3 = cotask.Task(task3_fun, name="Task_3", priority=3, period=10, profile=True, trace=False, shares=(q0))

    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
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
