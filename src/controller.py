from typing import Dict, Any
from pyPS4Controller.controller import Controller
from src.utils import normalise_to_range


class UGVRemoteController(Controller):
    """
    Converts PS4 Controller events to actionable commands for the UGV system.

    This class extends the `Controller` class from `pyPS4Controller` to interpret
    PS4 controller inputs and map them to UGV commands like speed and turn value.
    """

    def __init__(self, config: Dict[str, Any], **kwargs: Any) -> None:
        """
        Initialize the UGVRemoteController.

        Args:
            config: Configuration dictionary with PS4 controller and UGV parameters.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(
            interface=config["ps4_controller_config"]["PS4_INTERFACE"],
            connecting_using_ds4drv=False,
            **kwargs
        )
        self.config: Dict[str, Any] = config
        self.debug: bool = False  # debug event stream

        self.recording: bool = False
        self._speed: float = 0.0
        self._turn: int = 0.0

    @property
    def speed(self) -> float:
        """
        Getter for the right speed attribute.

        Returns:
            float: Current speed of the right motor.
        """
        return self._speed

    @property
    def turn(self) -> int:
        """
        Getter for the turn attribute.

        Returns:
            int: turning value (0.0: straight, -1.0: full left, 1.0: full right).
        """
        return self._turn

    @speed.setter
    def speed(self, val: float) -> None:
        """
        Setter for the right speed attribute.

        Args:
            val: New speed value for the right motor.
        """
        self._speed = val

    @turn.setter
    def turn(self, val: int) -> None:
        """
        Setter for the turn attribute.

        Args:
            val: New turn value (0.0: straight, -1.0: full left, 1.0: full right).
        """
        self._turn = val

    def on_R2_press(self, val: int) -> None:
        """
        Event handler for pressing the R2 button.

        Args:
            val: The pressure value of the R2 button.
        """
        speed: float = normalise_to_range(
            val,
            self.config["ps4_controller_config"]["R2_MIN"],
            self.config["ps4_controller_config"]["R2_MAX"],
            self.config["ugv_config"]["SPEED_MIN"],
            self.config["ugv_config"]["SPEED_MAX"],
        )
        self.speed = speed

    def on_R2_release(self) -> None:
        """
        Event handler for releasing the R2 button.

        Sets the left motor speed to 0.
        """
        self.speed = 0.0

    def on_L2_press(self, val: int) -> None:
        """
        Event handler for pressing the L2 button.

        Args:
            val: The pressure value of the L2 button.
        """
        speed: float = normalise_to_range(
            val,
            self.config["ps4_controller_config"]["L2_MIN"],
            self.config["ps4_controller_config"]["L2_MAX"],
            self.config["ugv_config"]["SPEED_MIN"],
            self.config["ugv_config"]["SPEED_MAX"],
        )
        speed = -speed  # reverse
        self.speed = speed

    def on_L2_release(self) -> None:
        """
        Event handler for releasing the L2 button.

        Sets the right motor speed to 0.
        """
        self.speed = 0.0

    def on_L3_right(self, val: int) -> None:
        """
        Event handler for pressing the L3 analogue right.

        Args:
            val: The pressure value of the L3 analogue.
        """
        turn: int = normalise_to_range(
            val,
            self.config["ps4_controller_config"]["L3_RIGHT_MIN"],
            self.config["ps4_controller_config"]["L3_RIGHT_MAX"],
            self.config["ugv_config"]["TURN_VALUE_MID"],
            self.config["ugv_config"]["TURN_VALUE_MAX"],
        )
        self.turn = turn

    def on_L3_left(self, val: int) -> None:
        """
        Event handler for pressing the L3 analogue left.

        Args:
            val: The pressure value of the L3 analogue.
        """
        turn: int = normalise_to_range(
            val,
            self.config["ps4_controller_config"]["L3_LEFT_MIN"],
            self.config["ps4_controller_config"]["L3_LEFT_MAX"],
            self.config["ugv_config"]["TURN_VALUE_MIN"],
            self.config["ugv_config"]["TURN_VALUE_MID"],
        )
        self.turn = turn

    def on_options_release(self) -> None:
        """
        Event handler for releasing the options button.

        Stops the controller.
        """
        self.stop = True

    def on_square_release(self) -> None:
        """
        Event handler for releasing the square button.

        Toggles recording.
        """
        self.recording = not self.recording

    def _ignore_event(self, *args: Any, **kwargs: Any) -> None:
        """
        Placeholder method to ignore events for unneeded buttons.

        Args:
            *args: Positional arguments for the event.
            **kwargs: Keyword arguments for the event.
        """
        pass

    # Ignore all other buttons
    on_x_press = _ignore_event
    on_x_release = _ignore_event
    on_triangle_press = _ignore_event
    on_triangle_release = _ignore_event
    on_circle_press = _ignore_event
    on_circle_release = _ignore_event
    on_square_press = _ignore_event
    on_L1_press = _ignore_event
    on_L1_release = _ignore_event
    on_R1_press = _ignore_event
    on_R1_release = _ignore_event
    on_up_arrow_press = _ignore_event
    on_up_down_arrow_release = _ignore_event
    on_down_arrow_press = _ignore_event
    on_left_arrow_press = _ignore_event
    on_left_right_arrow_release = _ignore_event
    on_right_arrow_press = _ignore_event
    on_L3_up = _ignore_event
    on_L3_down = _ignore_event
    on_L3_y_at_rest = _ignore_event
    on_L3_x_at_rest = _ignore_event
    on_L3_press = _ignore_event
    on_L3_release = _ignore_event
    on_R3_up = _ignore_event
    on_R3_down = _ignore_event
    on_R3_left = _ignore_event
    on_R3_right = _ignore_event
    on_R3_y_at_rest = _ignore_event
    on_R3_x_at_rest = _ignore_event
    on_R3_press = _ignore_event
    on_R3_release = _ignore_event
    on_options_press = _ignore_event
    on_share_press = _ignore_event
    on_share_release = _ignore_event
    on_playstation_button_press = _ignore_event
    on_playstation_button_release = _ignore_event
