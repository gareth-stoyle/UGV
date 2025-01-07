from pyPS4Controller.controller import Controller

class UGVRemoteController(Controller):
    """
    Converts PS4 Controller events to actionable commands for the UGV system.

    This class extends the `Controller` class from `pyPS4Controller` to interpret
    PS4 controller inputs and map them to UGV commands like speed and turn angle.
    """

    def __init__(self, config, **kwargs):
        """
        Initialize the UGVRemoteController.

        Args:
            config: Configuration dictionary with PS4 controller and UGV parameters.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(interface=config['ps4_controller_config']['PS4_INTERFACE'],
                         connecting_using_ds4drv=False,
                         **kwargs)
        self.config = config
        self.debug = False  # debug event stream
        # L3 & R3 spit out annoying output
        self.black_listed_buttons = [1, 4, 3]

        # Making these attrs properties may be overkill, but potentially
        # useful later on.
        self._speed = 0
        self._turn_angle = 0

    @property
    def speed(self):
        """
        Getter for the right speed attribute.

        Returns:
            float: Current speed of the right motor.
        """
        return self._speed

    @property
    def turn_angle(self):
        """
        Getter for the turn_angle attribute.

        Returns:
            int: turning angle (0: straight, -1: full left, 1: full right).
        """
        return self._turn_angle
    
    @speed.setter
    def speed(self, val):
        """
        Setter for the right speed attribute.

        Args:
            val: New speed value for the right motor.
        """
        self._speed = val

    @turn_angle.setter
    def turn_angle(self, val):
        """
        Setter for the turn_angle attribute.

        Args:
            int: new angle (0: straight, -1: full left, 1: full right).
        """
        self._turn_angle = val

    def _control_normalise(self, val, from_range, to_range):
        """
        Normalize a value from one range to another.

        Args:
            val: Input value to normalize.
            from_range: Tuple defining the input range (min, max).
            to_range: Tuple defining the target range (min, max).

        Returns:
            float: Normalized value rounded to 3 decimal places.
        """
        from_range_size = from_range[1] - from_range[0]
        val_dist_from_min = val - from_range[0]
        to_range_size = to_range[1] - to_range[0]
        val_ratio = val_dist_from_min / from_range_size

        if to_range[0] != 0:
            val = val_ratio * (to_range_size / to_range[0])
        else:
            val = val_ratio * to_range_size

        return round(val, 3)

    def on_R2_press(self, val):
        """
        Event handler for pressing the R2 button.

        Args:
            val: The pressure value of the R2 button.
        """
        speed = self._control_normalise(
            val,
            [self.config['ps4_controller_config']['R2_MIN'], self.config['ps4_controller_config']['R2_MAX']],
            [self.config['ugv_config']['SPEED_MIN'], self.config['ugv_config']['SPEED_MAX']]
        )
        self.speed = speed

    def on_R2_release(self):
        """
        Event handler for releasing the R2 button.

        Sets the left motor speed to 0.
        """
        self.speed = 0

    def on_L2_press(self, val):
        """
        Event handler for pressing the L2 button.

        Args:
            val: The pressure value of the L2 button.
        """
        speed = self._control_normalise(
            val,
            [self.config['ps4_controller_config']['L2_MIN'], self.config['ps4_controller_config']['L2_MAX']],
            [self.config['ugv_config']['SPEED_MIN'], self.config['ugv_config']['SPEED_MAX']]
        )
        speed = -speed # reverse
        self.speed = speed

    def on_L2_release(self):
        """
        Event handler for releasing the L2 button.

        Sets the right motor speed to 0.
        """
        self.speed = 0

    def on_L3_right(self, val):
        """
        Event handler for pressing the L3 analogue right.

        Args:
            val: The pressure value of the L3 analogue.
        """
        angle = self._control_normalise(
            val,
            [self.config['ps4_controller_config']['L3_RIGHT_MIN'], self.config['ps4_controller_config']['L3_RIGHT_MAX']],
            [self.config['ugv_config']['TURN_ANGLE_MID'], self.config['ugv_config']['TURN_ANGLE_MAX']]
        )
        self.turn_angle = angle

    def on_L3_left(self, val):
        """
        Event handler for pressing the L3 analogue left.

        Args:
            val: The pressure value of the L3 analogue.
        """
        angle = self._control_normalise(
            val,
            [self.config['ps4_controller_config']['L3_LEFT_MIN'], self.config['ps4_controller_config']['L3_LEFT_MAX']],
            [self.config['ugv_config']['TURN_ANGLE_MIN'], self.config['ugv_config']['TURN_ANGLE_MID']]
        )
        self.turn_angle = angle

    def _ignore_event(self, *args, **kwargs):
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
    on_square_release = _ignore_event
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
    on_options_release = _ignore_event
    on_share_press = _ignore_event
    on_share_release = _ignore_event
    on_playstation_button_press = _ignore_event
    on_playstation_button_release = _ignore_event
