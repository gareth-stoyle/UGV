from base_ctrl import BaseController
import time

###
# https://www.waveshare.com/wiki/UGV01#JSON_Command_Set
###

# Function for Detecting Raspberry Pi
def is_raspberry_pi5():
    with open('/proc/cpuinfo', 'r') as file:
        for line in file:
            if 'Model' in line:
                if 'Raspberry Pi 5' in line:
                    return True
                else:
                    return False

# Determine the GPIO Serial Device Name Based on the Raspberry Pi Model
if is_raspberry_pi5():
    base = BaseController('/dev/ttyAMA0', 115200)
else:
    base = BaseController('/dev/serial0', 115200)

# T is command type

# The wheel rotates at a speed of 0.2 meters per second and stops after 2 seconds.
# base.send_command({"T":1,"L":0.2,"R":0.2})
# time.sleep(2)
# base.send_command({"T":1,"L":0,"R":0})
# time.sleep(2)
# base.send_command({"T":1,"L":-0.2,"R":-0.2})
# time.sleep(2)
# base.send_command({"T":1,"L":0,"R":0})

# The X value is the moving linear velocity in m/s and the Z value is the steering angular velocity in rad/s.
# base.send_command({"T":13,"X":0.1,"Z":0.3})
# time.sleep(2)
# base.send_command({"T":13,"X":0,"Z":0})

# base.send_command({"T":3,"lineNum":0,"Text":"putYourTextHere"})
# time.sleep(2)
# base.send_command({"T":-3}) # not working?
