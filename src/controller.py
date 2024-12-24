from pyPS4Controller.controller import Controller

controller_config = {
    "R2_max_val": 32767,
    "R2_min_val": -32767,
    "L2_max_val": 32767,
    "L2_min_val": -32767
}

ugv_config = {
    # reverse or forward speed
    "speed_max_val": 1,
    "speed_min_val": 0
}

class UGVRemoteController(Controller):
    """Converts PS4 Controller events to actionable commands for UGV system"""

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.debug = False # debug event stream
        self.black_listed_buttons = [0, 1, 4, 3]

    def control_normalise(self, val, from_range, to_range):
        """
        Normalise values from one range to another.

        Returns: val, the value after normalisation, 3 decimal places.

        E.g control_normalise(self, 9804, [-32767, 32767], [0, 1])
            results in a val of 0.649
        """
        from_range_size = from_range[1] - from_range[0]
        val_dist_from_min = val - from_range[0]
        to_range_size = to_range[1] - to_range[0]
        # calc ratio of value in within from_range
        val_ratio = val_dist_from_min / from_range_size

        # calc speed by applying ratio to the to_range
        if to_range[0] != 0:
            val = val_ratio * (to_range_size / to_range[0])
        else:
            val = val_ratio * to_range_size
        
        return round(val, 3)

    def on_R2_press(self, val):
        speed = self.control_normalise(val, 
                                       [self.config.controller_config["R2_min_val"], self.config.controller_config["R2_max_val"]], 
                                       [self.config.ugv_config["speed_min_val"], self.config.ugv_config["speed_max_val"]])
        print(f"val: {val}, speed: {speed}")
        # need to run the below from UGVSystem drive method
        # # this needs to set system speed of a larger UGVSystem, which is continuously sending the ugv commands
        # self.base.send_command({"T":1,"L":speed,"R":speed})

    def on_R2_release(self):
        pass
        # need to run the below from UGVSystem drive method
        # self.base.send_command({"T":1,"L":0,"R":0})

    def on_L2_press(self, val):
        speed = self.control_normalise(val, 
                                       [self.config.controller_config["L2_min_val"], self.config.controller_config["L2_max_val"]], 
                                       [self.config.ugv_config["speed_min_val"], self.config.ugv_config["speed_max_val"]])
        speed = -speed # for reverse
        print(f"val: {val}, speed: {speed}")
        # need to run the below from UGVSystem drive method
        # self.base.send_command({"T":1,"L":speed,"R":speed})

    def on_L2_release(self):
        pass
        # need to run the below from UGVSystem drive method
        # self.base.send_command({"T":1,"L":0,"R":0})

    def _ignore_event(self, *args, **kwargs):
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
    on_L3_left = _ignore_event
    on_L3_right = _ignore_event
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

if __name__ == "__main__":
    pass