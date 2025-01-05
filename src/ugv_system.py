from threading import Thread
import time

from src.controller import UGVRemoteController
from src.base_ctrl import BaseController
from src.logger import customLogger

class UGVSystem:
    """High Level Controller for the system (remote control + UGV)"""

    def __init__(self, config, base_path):
        """
        Initialize the UGVSystem with configuration and base path.

        Args:
            config: Configuration dictionary for the remote controller.
            base_path: Path to the base device connection.
        """
        self.config = config
        self.base_path = base_path
        self.controller = UGVRemoteController(config=config)
        self.base = BaseController(base_path, 115200)
        self.logger = customLogger("ugv_system")
        self.logger.debug("Initialised UGVRemoteController and BaseController")

    def loop(self):
        """
        Main system loop to send commands to the UGV based on remote controller input.
        Logs output at a reduced frequency.
        """
        log_freq = 0.5  # Frequency of logging in seconds
        last_log = time.time()
        while True:
            # Determine if it's time to log
            log = False
            if (time.time() - last_log) > log_freq:
                log = True
                last_log = time.time()

            # Drive the UGV using current remote controller inputs
            self.drive(self.controller.r_speed, 
                       self.controller.l_speed, 
                       self.controller.direction,
                       log=log)

            time.sleep(0.01)  # Sleep to reduce CPU usage

    def drive(self, r_speed, l_speed, direction, log=False):
        """
        Send drive commands to the UGV.

        Args:
            r_speed: Right wheel speed.
            l_speed: Left wheel speed.
            direction: Driving direction (0 for reverse, 1 for forward).
            log: Flag to indicate if the command should be logged.
        """
        if direction == 0:
            # Reverse direction by inverting speeds
            r_speed = -r_speed
            l_speed = -l_speed

        if log:
            self.logger.debug(f"Drive Command OUT: r_speed: {r_speed}, "
                              f"l_speed: {l_speed}, direction: {direction}")

        # Send the command to the base controller
        self.base.send_command({"T": 1, "R": r_speed, "L": l_speed})

    def run(self):
        """
        Start the system threads for remote control and main loop.
        Ensures the UGV stops when the remote control thread ends.
        """
        # Thread to handle remote control listening
        remote_control_thread = Thread(target=self.controller.listen, args=(60,))
        # Thread to handle the system's main loop
        system_loop_thread = Thread(target=self.loop)

        remote_control_thread.start()
        system_loop_thread.start()

        remote_control_thread.join()

        # Stop the UGV when remote control ends
        self.logger.debug("Remote control thread ended, ensuring UGV stopped")
        self.drive(0, 0, 1)
        self.controller.r_speed = 0
        self.controller.l_speed = 0

        system_loop_thread.join()


if __name__ == "__main__":
    pass
