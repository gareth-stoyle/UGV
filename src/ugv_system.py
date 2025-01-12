import keyboard
from threading import Thread
import time

from src.controller import UGVRemoteController
from src.base_ctrl import BaseController
from src.logger import customLogger

class UGVSystem:
    """High Level Controller for the system (remote control + UGV)"""

    def __init__(self, config, base_path, debug_logging):
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
        self.logger = customLogger("ugv_system", "log/app.log", debug_logging)
        self.logger.debug("Initialised UGVRemoteController and BaseController")

    def _drive(self, speed, turn, log=False):
        """
        Send drive commands to the UGV.

        Args:
            speed: Overall speed, ranges from -0.5 (reverse) to +0.5 (forward).
            turn: Turning value, ranges from -1 (sharp left) to +1 (sharp right).
            log: Flag to indicate if the command should be logged.
        """
        if log:
            self.logger.debug(f"Drive Command OUT 1: speed: {speed}, "
                              f"turn: {turn}")

        r_speed, l_speed = self._calculate_track_speeds(speed, turn)

        # Send the command to the base controller
        self.base.send_command({"T": 1, "R": r_speed, "L": l_speed})

        if log:
            self.logger.debug(f"Drive Command OUT 2: r_speed: {r_speed}, "
                              f"l_speed: {l_speed}")

    @staticmethod
    def _calculate_track_speeds(speed, turn):
        """
        Calculate left and right track speeds for a tracked vehicle.
        Adjustment is required when the moving vehicle is turning.

        Args:
            speed: Overall speed, ranges from -0.5 (reverse) to +0.5 (forward).
            turn: Turning value, ranges from -1 (sharp left) to +1 (sharp right).
        """
        # no adjustment needed when stationary or driving straight.
        if speed == 0 or turn == 0:
            return speed, speed

        # Turning right, reduce left track speed.
        if turn > 0:
            l_speed = speed * (1 - turn)
            r_speed = speed
        # Turning left, reduce right track speed.
        elif turn < 0:
            l_speed = speed
            r_speed = speed * (1 + turn)

        return l_speed, r_speed

    def _loop(self):
        """
        Main system loop to send commands to the UGV based on remote controller input.
        Logs output at a reduced frequency.
        """
        log_freq = 0.5  # Frequency of logging in seconds
        last_log = time.time()
        while not self.controller.stop:
            # Determine if it's time to log
            log = False
            if (time.time() - last_log) > log_freq:
                log = True
                last_log = time.time()

            # Drive the UGV using current remote controller inputs
            self._drive(self.controller.speed,
                       self.controller.turn,
                       log=log)

            time.sleep(0.01)  # Sleep to reduce CPU usage
        if self.controller.stop:
            self.logger.info("Stop command received, exiting!")

    def run(self):
        """
        Start the system threads for remote control and main loop.
        Ensures the UGV stops when the remote control thread ends.
        """
        # Thread to handle remote control listening
        remote_control_thread = Thread(target=self.controller.listen, args=(60,))
        # Thread to handle the system's main loop
        system_loop_thread = Thread(target=self._loop)

        remote_control_thread.start()
        system_loop_thread.start()

        remote_control_thread.join()

        # Stop the UGV system if remote control ends abruptly (battery/connection)
        self.logger.debug("Remote control thread ended, ensuring UGV stopped")
        self._drive(0, 0, 1)
        self.controller.speed = 0

        system_loop_thread.join()


if __name__ == "__main__":
    pass
