import pytest
from threading import Thread
from unittest.mock import MagicMock, patch

from config.config import config
from src.ugv_system import UGVSystem
from src.controller import UGVRemoteController
from src.base_ctrl import BaseController
from src.utils import is_raspberry_pi5

# Determine the GPIO Serial Device Name Based on the Raspberry Pi Model
base_path = '/dev/ttyAMA0' if is_raspberry_pi5() else '/dev/serial0'

# 1. Test Initialization
def test_initialization():
    init_test_system = UGVSystem(config=config, base_path=base_path)
    assert isinstance(init_test_system.controller, UGVRemoteController)
    assert isinstance(init_test_system.base, BaseController)

# Setup global system and replace basecontroller and logger with mocks
system = UGVSystem(config=config, base_path=base_path)
mock_base = MagicMock()
mock_logger = MagicMock()
system.base = mock_base
system.logger = mock_logger

# 2. Test `drive` Method
def test_drive():
    # Test forward drive
    system.drive(0.5, 0.5, 1, log=True)
    system.base.send_command.assert_called_with({"T": 1, "R": 0.5, "L": 0.5})

    # Test reverse drive
    system.drive(-0.5, -0.5, 1, log=True)
    system.base.send_command.assert_called_with({"T": 1, "R": -0.5, "L": -0.5})


# I need to add a nice flag to stop the loop and controller thread,
# then testing loop and run will be easier

# 3. Test `loop` Method
# def test_loop():

#     system_loop_thread = Thread(target=system.loop)
#     system_loop_thread.start()

# # 4. Test `run` Method
# def test_run():
    # pass
