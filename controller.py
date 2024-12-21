from pyPS4Controller.controller import Controller
from base_ctrl import BaseController
import time

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

# # The wheel rotates at a speed of 0.2 meters per second and stops after 2 seconds.
# base.send_command({"T":1,"L":0.2,"R":0.2})
# time.sleep(1)
# base.send_command({"T":1,"L":0,"R":0})
# time.sleep(2)
# base.send_command({"T":1,"L":-0.2,"R":-0.2})
# time.sleep(2)
# base.send_command({"T":1,"L":0,"R":0})


class UGVController(Controller):
    def __init__(self, base, controller_config, ugv_config, **kwargs):
        super().__init__(**kwargs)
        self.base = base
        self.controller_config = controller_config
        self.ugv_config = ugv_config

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
                                       [controller_config["R2_min_val"], controller_config["R2_max_val"]], 
                                       [ugv_config["speed_min_val"], ugv_config["speed_max_val"]])
        print(f"val: {val}, speed: {speed}")
        self.base.send_command({"T":1,"L":speed,"R":speed})

    def on_R2_release(self):
        self.base.send_command({"T":1,"L":0,"R":0})

    def on_L2_press(self, val):
        speed = self.control_normalise(val, 
                                       [controller_config["L2_min_val"], controller_config["L2_max_val"]], 
                                       [ugv_config["speed_min_val"], ugv_config["speed_max_val"]])
        speed = -speed # for reverse
        print(f"val: {val}, speed: {speed}")
        self.base.send_command({"T":1,"L":speed,"R":speed})

    def on_L2_release(self):
        self.base.send_command({"T":1,"L":0,"R":0})

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
        base = BaseController('/dev/ttyAMA0', 115200)
    else:
        base = BaseController('/dev/serial0', 115200)

    # connect to parent Controller class for understanding default behaviour
    # controller = Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)

    controller = UGVController(interface="/dev/input/js0", 
                               connecting_using_ds4drv=False, 
                               base=base, 
                               controller_config=controller_config, 
                               ugv_config=ugv_config)
    
    # you can start listening before controller is paired, as long as you pair it within the timeout window
    controller.listen(timeout=60)
