from pyPS4Controller.controller import Controller

class UGVRemoteController(Controller):
    """
    Converts PS4 Controller events to actionable commands for the UGV system.

    This class extends the `Controller` class from `pyPS4Controller` to interpret
    PS4 controller inputs and map them to UGV commands like speed and direction.
    """

    def __init__(self, config, **kwargs):
        """
        Initialize the UGVRemoteController.

        Args:
            config: Configuration dictionary with PS4 controller and UGV parameters.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(interface=config['ps4_controller_config']['ps4_interface'],
                         connecting_using_ds4drv=False,
                         **kwargs)
        self.config = config
        self.debug = False  # debug event stream
        # L3 & R3 spit out annoying output
        self.black_listed_buttons = [0, 1, 4, 3]

        # Making these attrs properties may be overkill, but potentially
        # useful later on.
        self._r_speed = 0
        self._l_speed = 0
        self._direction = 1

    @property
    def r_speed(self):
        """
        Getter for the right speed attribute.

        Returns:
            float: Current speed of the right motor.
        """
        return self._r_speed

    @property
    def l_speed(self):
        """
        Getter for the left speed attribute.

        Returns:
            float: Current speed of the left motor.
        """
        return self._l_speed

    @property
    def direction(self):
        """
        Getter for the direction attribute.

        Returns:
            int: Current direction (1 for forward, 0 for backward).
        """
        return self._direction

    @r_speed.setter
    def r_speed(self, val):
        """
        Setter for the right speed attribute.

        Args:
            val: New speed value for the right motor.
        """
        self._r_speed = val

    @l_speed.setter
    def l_speed(self, val):
        """
        Setter for the left speed attribute.

        Args:
            val: New speed value for the left motor.
        """
        self._l_speed = val

    @direction.setter
    def direction(self, val):
        """
        Setter for the direction attribute.

        Args:
            val: New direction value (1 for forward, 0 for backward).
        """
        self._direction = val

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
            [self.config['ps4_controller_config']['R2_min_val'], self.config['ps4_controller_config']['R2_max_val']],
            [self.config['ugv_config']['speed_min_val'], self.config['ugv_config']['speed_max_val']]
        )
        self.l_speed = speed

    def on_R2_release(self):
        """
        Event handler for releasing the R2 button.

        Sets the left motor speed to 0.
        """
        self.l_speed = 0

    def on_L2_press(self, val):
        """
        Event handler for pressing the L2 button.

        Args:
            val: The pressure value of the L2 button.
        """
        speed = self._control_normalise(
            val,
            [self.config['ps4_controller_config']['L2_min_val'], self.config['ps4_controller_config']['L2_max_val']],
            [self.config['ugv_config']['speed_min_val'], self.config['ugv_config']['speed_max_val']]
        )
        self.r_speed = speed

    def on_L2_release(self):
        """
        Event handler for releasing the L2 button.

        Sets the right motor speed to 0.
        """
        self.r_speed = 0

    def on_triangle_release(self):
        """
        Event handler for releasing the Triangle button.

        Toggles the direction attribute (1 for forward, 0 for backward).
        """
        self.direction = self.direction ^ 1

    def _ignore_event(self, *args, **kwargs):
        """
        Placeholder method to ignore events for unneeded buttons.

        Args:
            *args: Positional arguments for the event.
            **kwargs: Keyword arguments for the event.
        """
        pass
