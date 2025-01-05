from config.config import config
from src.ugv_system import UGVSystem
from src.utils import is_raspberry_pi5

# Determine the GPIO Serial Device Name Based on the Raspberry Pi Model
base_path = '/dev/ttyAMA0' if is_raspberry_pi5() else '/dev/serial0'

system = UGVSystem(config=config, base_path=base_path)
system.run()