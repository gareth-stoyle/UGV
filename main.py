from src.ugv_system import UGVSystem
from src.utils import is_raspberry_pi5

# Determine the GPIO Serial Device Name Based on the Raspberry Pi Model
if is_raspberry_pi5():
    base_path = '/dev/ttyAMA0'
else:
    base_path = '/dev/serial0'

config = {
    "controller_config": {
        "ps4_interface": "/dev/input/js0",
        "R2_max_val": 32767,
        "R2_min_val": -32767,
        "L2_max_val": 32767,
        "L2_min_val": -32767
    },
    "ugv_config": {
        # reverse and forward speed
        "speed_max_val": 0.5,
        "speed_min_val": 0
    }
}

system = UGVSystem(config=config, base_path=base_path)
system.run()