from threading import Thread
import time
from typing import Dict, Any, Tuple

from src.base_ctrl import BaseController
from src.camera import Camera
from src.controller import UGVRemoteController
from src.logger import customLogger


class UGVSystem:
    """High Level Controller for the system (remote control + UGV)"""

    def __init__(
        self,
        config: Dict[str, Any],
        base_path: str,
        debug_logging: bool,
        camera: bool = False,
    ) -> None:
        """
        Initialize the UGVSystem with configuration and base path.

        Args:
            config: Configuration dictionary for the remote controller.
            base_path: Path to the base device connection.
            debug_logging: Flag to enable or disable debug-level logging.
            camera: Whether to initialise a camera.
        """
        self.config = config
        self.base_path = base_path
        self.is_recording: bool = False
        self.base = BaseController(base_path, 115200)
        self.controller = UGVRemoteController(config=config)
        self.logger = customLogger("ugv_system", "outputs/log/app.log", debug_logging)
        self.logger.debug("Initialised UGVRemoteController, BaseController")
        if camera:
            self.camera = Camera(resolution=(1920, 1080), flip=False)
            self.logger.debug("Initialised Camera")

    def _drive(self, speed: float, turn: float, log: bool = False) -> None:
        """
        Send drive commands to the UGV.

        Args:
            speed: Overall speed, ranges from -0.5 (reverse) to +0.5 (forward).
            turn: Turning value, ranges from -1 (sharp left) to +1 (sharp right).
            log: Flag to indicate if the command should be logged.
        """
        if log:
            self.logger.debug(f"Drive Command OUT 1: speed: {speed}, turn: {turn}")

        r_speed, l_speed = self._calculate_track_speeds(speed, turn)

        # Send the command to the base controller
        self.base.send_command({"T": 1, "R": r_speed, "L": l_speed})

        if log:
            self.logger.debug(
                f"Drive Command OUT 2: r_speed: {r_speed}, l_speed: {l_speed}"
            )

    @staticmethod
    def _calculate_track_speeds(speed: float, turn: float) -> Tuple[float, float]:
        """
        Calculate left and right track speeds for a tracked vehicle.
        Adjustment is required when the moving vehicle is turning.

        Args:
            speed: Overall speed, ranges from -0.5 (reverse) to +0.5 (forward).
            turn: Turning value, ranges from -1 (sharp left) to +1 (sharp right).

        Returns:
            Tuple[float, float]: Calculated left and right track speeds.
        """
        # No adjustment needed when stationary or driving straight.
        if speed == 0.0 or turn == 0.0:
            return speed, speed

        # Turning right, reduce left track speed.
        if turn > 0.0:
            l_speed = speed * (1 - turn)
            r_speed = speed
        # Turning left, reduce right track speed.
        elif turn < 0.0:
            l_speed = speed
            r_speed = speed * (1 + turn)

        return l_speed, r_speed

    def _toggle_camera_recording(self):
        """Toggles camera recording."""
        video_name = f"video_{time.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
        if self.is_recording:
            self.camera.stop_recording()
            self.logger.info("Stopped camera recording.")
        else:
            self.camera.start_recording(
                self.config["general_config"]["VIDEO_PATH"], video_name
            )
            self.logger.info("Started camera recording.")
        self.is_recording = not self.is_recording

    def _terminate(self) -> None:
        """Kill system by killing controller"""
        self.controller.stop = True

    def _loop(self) -> None:
        """
        Main system loop to send commands to the UGV based on remote controller input.
        Logs output at a reduced frequency.
        """
        log_freq: float = 0.5  # Frequency of logging in seconds
        last_log: float = time.time()
        while not self.controller.stop:
            # Determine if it's time to log
            log: bool = False
            if (time.time() - last_log) > log_freq:
                log = True
                last_log = time.time()

            # Drive the UGV using current remote controller inputs
            self._drive(self.controller.speed, self.controller.turn, log=log)

            if self.is_recording != self.controller.recording:
                self._toggle_camera_recording()

            time.sleep(0.01)  # Sleep to reduce CPU usage

        if self.controller.stop:
            self.logger.info("Stop command received, exiting!")
            self._drive(0.0, 0.0, True)
            self.controller.speed = 0.0

    def run(self) -> None:
        """
        Start the system threads for remote control and main loop.
        Ensures the UGV stops when the remote control thread ends.
        """
        # Thread to handle remote control listening
        remote_control_thread: Thread = Thread(
            target=self.controller.listen, args=(60,)
        )
        # Thread to handle the system's main loop
        system_loop_thread: Thread = Thread(target=self._loop)

        remote_control_thread.start()
        system_loop_thread.start()

        remote_control_thread.join()

        # Stop the UGV system if remote control ends abruptly (battery/connection)
        self.logger.debug("Remote control thread ended, ensuring UGV stopped")
        self._drive(0.0, 0.0, True)
        self.controller.speed = 0.0

        system_loop_thread.join()


if __name__ == "__main__":
    pass
