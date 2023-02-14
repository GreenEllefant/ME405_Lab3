"""! @file position_control.py
    This file contains the Position Control class
    
    @author Jack Ellsworth, Hannah Howe, Mathew Smith
    @date   05-Feb-2023
    @copyright (c) 2023 by Nobody and released under GNU Public License v3
"""
import utime

class Position_Control:
    """! 
    This class implements a closed loop position control for a motor
    """
    def __init__(self, gain, setpoint, encoder, motor):
        """! 
        Creates a closed loop by initializing values
        used for closed loop control.
        @param gain: sets the gain from the controller
        @param setpoint: sets the initial setpoint for the controller
        @param encoder: takes an encoder_reader class for the system
        @param motor: takes a motor_driver class for the system
        """
        self.gain = gain
        self.setpoint = setpoint
        self.values = [0,0]
        self.encoder = encoder
        self.motor = motor
        self.time = utime.ticks_ms()

    def run(self, setpoint):
        """! 
        Updates the system parameters
        @param gain sets the gain from the controller
        @param setpoint sets the initial setpoint for the controller
        @param encoder takes an encoder_reader class for the system
        @param motor takes a motor_driver class for the system
        """
        self.setpoint = setpoint
        self.values[0] = (utime.ticks_ms() - self.time)
        self.values[1] = (self.encoder.read())
        self.motor.set_duty_cycle(self.gain * (self.setpoint - self.encoder.read()))

    def reset_values(self):
        """! 
        Resets the system values and time
        """
        self.values = [0,0]
        self.time = utime.ticks_ms()

    def set_setpoint(self, setpoint):
        """!
        Sets a new setpoint
        @param setpoint The new setpoint
        """
        self.setpoint = setpoint
    
    def set_Kp(self, gain):
        """!
        Sets a new controller gain
        @param gain The new controller gain
        """
        self.gain = gain