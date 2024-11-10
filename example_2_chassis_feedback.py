from base_ctrl import BaseController
import json

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

# Implement an infinite loop to continuously monitor serial port data.
while True:
    try:
        # Read a line of data from the serial port, decode it into a 'utf-8' formatted string, and attempt to convert it into a JSON object.
        data_recv_buffer = json.loads(base.rl.readline().decode('utf-8'))
        print(data_recv_buffer)
        # Check if the parsed data contains the key 'T'.
        # if 'T' in data_recv_buffer:
        #     # If the value of 'T' is 1001, print the received data and break out of the loop.
        #     if data_recv_buffer['T'] == 1001:
        #         print(data_recv_buffer)
        #         # break
    # If an exception occurs while reading or processing the data, ignore the exception and continue to listen for the next line of data.
    except Exception as e:
        print(e)
