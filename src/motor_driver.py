"""! @motor_driver.py
    This file contains a motor driver for an ME405 kit. 
    
    @author Jack Ellsworth, Hannah Howe, Mathew Smith
    @date   5-Feb-2023
    @copyright (c) 2023 by Nobody and released under GNU Public License v3
"""

import pyb
class Motor_Driver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin Encoder Pin for the Motor
        @param in1pin First Interrput Channel for the Motor
        @param in2pin Second Interrupt Channel for the Motor
        @param timer Timer Channel for the Motor
        """
        self.en_pin = en_pin
        self.in1pin = in1pin
        self.in2pin = in2pin
        self.timer = timer
        self.ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.in1pin)
        self.ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.in2pin)
        self.en_pin.high()
        self.ch1.pulse_width_percent(0)
        self.ch2.pulse_width_percent(0)
        print ("Creating a motor driver")

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        if(level > 0):
            self.ch1.pulse_width_percent(level)
            self.ch2.pulse_width_percent(0)
        elif(level < 0):
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(level*-1)
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)
    
if __name__ == "__main__":
    en_pin = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    in1pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    tim = pyb.Timer(5, prescaler = 0 , period = 0xFFFF)
    moe = Motor_Driver(en_pin, in1pin, in2pin, tim)
    moe.set_duty_cycle(90)
