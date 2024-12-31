from threading import Thread
import time

from controller import UGVRemoteController
from base_ctrl import BaseController

class UGVSystem:
    """High Level Controller for the system (remote control + UGV)"""

    def __init__(self, config, base_path):
        self.config = config
        self.base_path = base_path
        self.direction = 1 # 1 for forward, 0 for reverse
        self.r_speed = 0
        self.l_speed = 0

        self.controller = UGVRemoteController(config=config)
        self.base = BaseController(base_path, 115200)

        print("initialised controller and basecontroller")

    def loop(self):
        while True:
            self.r_speed = self.controller.r_speed
            self.l_speed = self.controller.l_speed
            self.direction = self.controller.direction
            self.drive(self.r_speed, self.l_speed, self.direction)
            time.sleep(0.01)

    def drive(self, r_speed, l_speed, direction):
        """Send UGV command to drive, given the speed and angle"""
        if direction == 0:
            # reverse
            r_speed = -r_speed
            l_speed = -l_speed

        # print(f"Sending drive command, r_speed = {r_speed}, l_speed = {l_speed}")
        self.base.send_command({"T":1,"R":r_speed,"L":l_speed})

    def run(self):
        remote_control_thread = Thread(target=self.controller.listen, 
                                                 args=(60,))
        system_loop_thread = Thread(target=self.loop)

        remote_control_thread.start()
        system_loop_thread.start()

        remote_control_thread.join()
        print("remote control thread ended, ensuring UGV stopped")
        self.controller.r_speed = 0
        self.controller.l_speed = 0
        system_loop_thread.join()


if __name__ == "__main__":
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

    config = {
        "controller_config": {
            "ps4_interface": "/dev/input/js0",
            "R2_max_val": 32767,
            "R2_min_val": -32767,
            "L2_max_val": 32767,
            "L2_min_val": -32767
        },
        "ugv_config": {
            # reverse or forward speed
            "speed_max_val": 1,
            "speed_min_val": 0
        }
    }
    system = UGVSystem(config=config, base_path=base_path)
    system.run()