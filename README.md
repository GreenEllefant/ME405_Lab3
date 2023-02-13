# ME 405 Lab 3
This directory conatins files for closed loop positional control of two motors simultainously. The position of the motors are then send to a plotter where the step response is plotted.

The motors are runs simlutaniously using the cotask library in the ME 405 support library. There are 3 tasks that run the motors, one for each motor to be run and one to send data to the plotter. The motor tasks are identical outside of the desired encoder position and which pins they control.

The motor tasks start by setting up the encoder and motor driver for each motor. These are then placed into a position control class where they are run to a desired position is reached. To simulate a step response, these are run for 5 seconds. Each time the controller is run, position and time data is placed into a queue as list of characters. After the 5 seconds is up, a -1 is placed into the time data slot to indicate that no new data is being sent.

The task that sends data waits for the queue to have values in it. If there is anything in the queue, it will send a character, then move to the next task. Since the data from the motor is longer than what this task can send, this task must run significantly faster so that the queue does not fill up and halt the running of other tasks.

If one motor is running too slow, the position in code will not reflect the actual position, causing the controller to miss the position completely. In our testing we found that running the motors any slower than a period of 75 creates an unstable response.

Below are the step responses of each motor running simultaneously. Motor 1 was attempting to reach a position of 8000 while motor 2 was attempting to reach a position of 5000. Each motor ran with a gain value of 0.05. Note that the time is in milliseconds rather than seconds.

<img width="490" alt="Impulse_response_motor1" src="https://user-images.githubusercontent.com/57115504/218598967-d1ffb12c-1384-4dd5-b2a8-7443c0a9964d.png">
Image of motor 1 impulse response

<img width="390" alt="Impulse_response_motor2" src="https://user-images.githubusercontent.com/57115504/218599051-6930a792-12e3-48e5-8377-3c79cfdda0b4.png">
Image of motor 2 impulse response
