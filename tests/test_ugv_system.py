from pytest import approx
from threading import Thread
import time
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
    init_test_system = UGVSystem(config=config, base_path=base_path, debug_logging=False)
    assert isinstance(init_test_system.controller, UGVRemoteController)
    assert isinstance(init_test_system.base, BaseController)

# Setup global system and replace basecontroller and logger with mocks
system = UGVSystem(config=config, base_path=base_path, debug_logging=False)
mock_base = MagicMock()
mock_logger = MagicMock()
system.base = mock_base
system.logger = mock_logger

# 2. Test `drive` Method
def test_drive():
    """Test the _drive method with various inputs."""
    # Test forward drive
    system._drive(0.5, 0, log=True)
    mock_base.send_command.assert_called_with({"T": 1, "R": 0.5, "L": 0.5})

    # Test reverse drive
    system._drive(-0.5, 0, log=True)
    mock_base.send_command.assert_called_with({"T": 1, "R": -0.5, "L": -0.5})

    # Test turning right
    system._drive(0.5, 1, log=True)
    mock_base.send_command.assert_called_with({"T": 1, "R": 0.0, "L": 0.5})

    # Test turning left
    system._drive(0.35, -0.5, log=True)
    mock_base.send_command.assert_called_with({"T": 1, "R": 0.35, "L": 0.175})

    # Test stationary with no turn
    system._drive(0, 0, log=True)
    mock_base.send_command.assert_called_with({"T": 1, "R": 0, "L": 0})

def test_calculate_track_speeds():
    """Test the _calculate_track_speeds method."""
    assert system._calculate_track_speeds(0.5, 0) == (0.5, 0.5), "Failed straight drive calculation."
    assert system._calculate_track_speeds(0.5, 1) == (0.0, 0.5), "Failed right turn calculation."
    assert system._calculate_track_speeds(0.5, -1) == (0.5, 0.0), "Failed left turn calculation."
    assert system._calculate_track_speeds(0, 0) == (0, 0), "Failed stationary calculation."
    assert system._calculate_track_speeds(0.5, 0.5) == (0.25, 0.5), "Failed gentle right turn calculation."
    assert system._calculate_track_speeds(0.5, -0.5) == (0.5, 0.25), "Failed gentle left turn calculation."
    assert system._calculate_track_speeds(1.0, -0.3) == (1.0, 0.7), "Failed left turn with higher speed calculation."
    assert system._calculate_track_speeds(0.2, 0.8) == approx((0.04, 0.2)), "Failed sharp right turn with low speed calculation."

# 4. Test `_terminate` Method
def test_terminate():
    """Test the _terminate method."""
    system._terminate()
    assert system.controller.stop is True, "Controller stop flag not set."

# 5. Test `_loop` Method
def test_loop():
    """Test the _loop method under controlled conditions."""
    # Simulate controller inputs
    system.controller.speed = 0.5
    system.controller.turn = 0
    system.controller.stop = False

    # Start the loop in a separate thread
    loop_thread = Thread(target=system._loop)
    loop_thread.start()

    # Allow some time for the loop to run
    time.sleep(1)

    mock_base.send_command.assert_called_with({"T": 1, "R": 0.5, "L": 0.5})
    # Terminate the loop and verify behavior
    system._terminate()
    loop_thread.join()

    # Verify final commands sent
    mock_base.send_command.assert_called_with({"T": 1, "R": 0, "L": 0})

# 6. Test `run` Method
def test_run():
    """Test the run method with mocked threads."""
    with patch("threading.Thread.start") as mock_start, \
         patch("threading.Thread.join") as mock_join:

        system.run()

        # Ensure threads were started and joined
        assert mock_start.call_count == 2, "Not all threads started."
        assert mock_join.call_count == 2, "Not all threads joined."