from src.controller import UGVRemoteController
from src.base_ctrl import BaseController

class UGVSystem:
    """High Level Controller for the system (remote control + UGV)"""

    def __init__(self, config, base_path):
        self.config = config
        self.base_path = base_path
        self.direction = 1 # 1 for forward, 0 for reverse
        self.speed = 0
        self.angle = 0 # turning direction

        self.controller = UGVRemoteController(config=config, 
                            connecting_using_ds4drv=False)
        self.base = BaseController(base_path, 115200)

        self.breath_light(15)

        print("initialised controller and basecontroller")
        # you can start listening before controller is paired, as long as you pair it within the timeout window
        # self.controller.listen(timeout=60)


    def loop(self):
        pass
        # while True:
        #     pass

    def drive(self, direction, speed, angle):
        """Send UGV command to drive, given the direction, speed and angle"""
        pass

    def breath_light(self, input_time):
        self.base.breath_light(input_time)