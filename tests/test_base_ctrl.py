import json
import pytest
import time
from unittest.mock import MagicMock, patch
from src.base_ctrl import BaseController

@pytest.fixture
def mock_serial():
    """Fixture to mock the serial.Serial class."""
    with patch("serial.Serial") as mock_serial_class:
        yield mock_serial_class

@pytest.fixture
def controller(mock_serial):
    """Fixture to create a BaseController instance with mocked serial."""
    mock_serial_instance = MagicMock()
    mock_serial.return_value = mock_serial_instance
    controller = BaseController(uart_dev_set='/dev/ttyUSB0', buad_set=115200)
    return controller

def test_initialization(controller, mock_serial):
    """Test initialization of the BaseController class."""
    mock_serial.assert_called_with('/dev/ttyUSB0', 115200, timeout=1)

    assert isinstance(controller, BaseController)

def test_send_command(controller):
    """Test that send_command adds commands to the queue."""
    data = {"command": "test"}
    
    # Call send_command method
    controller.send_command(data)

    # Check that the command is added to the queue
    assert controller.command_queue.qsize() == 1

def test_process_commands(controller, mock_serial):
    """Test that commands in the queue are sent via serial."""
    data = {"command": "test"}

    # Simulate the processing of commands
    controller.command_queue.put(data) 
    time.sleep(0.1)
    mock_serial.return_value.write.assert_called_once_with(
        (json.dumps(data) + '\n').encode("utf-8")
    )

def test_base_json_ctrl(controller):
    """Test that base_json_ctrl sends the correct data to the UART."""
    data = {"command": "test_json"}
    
    # Mock send_command to verify that base_json_ctrl calls it correctly
    with patch.object(controller, 'send_command') as mock_send_command:
        controller.base_json_ctrl(data)
        mock_send_command.assert_called_once_with(data)