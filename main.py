from src.ugv_system import UGVSystem

config = {
    "interface": '/dev/input/js0',
    "controller_config": {
        "R2_max_val": 32767,
        "R2_min_val": -32767,
        "L2_max_val": 32767,
        "L2_min_val": -32767
    },
    "ugv_config":{
        # reverse or forward speed
        "speed_max_val": 1,
        "speed_min_val": 0
    }
}

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
    base_path = '/dev/ttyAMA0'
else:
    base_path = '/dev/serial0'

ugv_system = UGVSystem(config=config, base_path=base_path)
ugv_system.loop()
