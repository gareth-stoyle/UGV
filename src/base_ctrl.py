import serial
import json
import queue
import threading


class BaseController:
    """
    A base controller class for managing communication over a UART interface
    and processing commands asynchronously.
    """

    def __init__(self, uart_dev_set, buad_set):
        """
        Initialize the BaseController with a UART device and baud rate.

        :param uart_dev_set: The UART device to connect to (e.g., '/dev/ttyUSB0').
        :param buad_set: The baud rate for the serial communication.
        """
        self.ser = serial.Serial(uart_dev_set, buad_set, timeout=1)
        self.command_queue = queue.Queue()
        self.command_thread = threading.Thread(
            target=self.process_commands, daemon=True
        )
        self.command_thread.start()

    def send_command(self, data):
        """
        Add a command to the queue for processing.

        :param data: The command data to send. Typically a dictionary or JSON-serializable object.
        """
        self.command_queue.put(data)

    def process_commands(self):
        """
        Continuously process commands from the queue and send them over the UART interface.
        """
        while True:
            data = self.command_queue.get()
            self.ser.write((json.dumps(data) + "\n").encode("utf-8"))

    def base_json_ctrl(self, input_json):
        """
        Send a JSON command to the UART device.

        :param input_json: The JSON data to send. Must be JSON-serializable.
        """
        self.send_command(input_json)
