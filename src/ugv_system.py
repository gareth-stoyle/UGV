from threading import Thread
import time

from src.controller import UGVRemoteController
from src.base_ctrl import BaseController
from src.logger import customLogger

class UGVSystem:
    """High Level Controller for the system (remote control + UGV)"""

    def __init__(self, config, base_path):
        self.config = config
        self.base_path = base_path
        self.controller = UGVRemoteController(config=config)
        self.base = BaseController(base_path, 115200)
        self.logger = customLogger("ugv_system")
        self.logger.debug("initialised UGVRemoteController and BaseController")

    def loop(self):
        log_freq = 0.5 # seconds
        last_log = time.time()
        while True:
            # reduce amount of logging output
            log = False
            if (time.time() - last_log) > log_freq:
                log = True
                last_log = time.time()
            
            self.drive(self.controller.r_speed, 
                       self.controller.l_speed, 
                       self.controller.direction,
                       log=log)

            time.sleep(0.01)

    def drive(self, r_speed, l_speed, direction, log=False):
        """Send UGV command to drive, given the speeds and direction"""
        if direction == 0:
            # reverse
            r_speed = -r_speed
            l_speed = -l_speed

        if log:
            self.logger.debug(f"Drive Command OUT: r_speed: {r_speed}, "
                              f"l_speed: {l_speed}, direction: {direction}")

        self.base.send_command({"T":1,"R":r_speed,"L":l_speed})

    def run(self):
        remote_control_thread = Thread(target=self.controller.listen, 
                                                 args=(60,))
        system_loop_thread = Thread(target=self.loop)

        remote_control_thread.start()
        system_loop_thread.start()

        remote_control_thread.join()

        self.logger.debug("remote control thread ended, ensuring UGV stopped")
        self.drive(0, 0, 1)
        self.controller.r_speed = 0
        self.controller.l_speed = 0

        system_loop_thread.join()


if __name__ == "__main__":
    pass