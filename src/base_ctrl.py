import serial  
import json
import queue
import threading


class BaseController:

	def __init__(self, uart_dev_set, buad_set):
		self.ser = serial.Serial(uart_dev_set, buad_set, timeout=1)
		self.command_queue = queue.Queue()
		self.command_thread = threading.Thread(target=self.process_commands, daemon=True)
		self.command_thread.start()

	def send_command(self, data):
		self.command_queue.put(data)

	def process_commands(self):
		while True:
			data = self.command_queue.get()
			self.ser.write((json.dumps(data) + '\n').encode("utf-8"))

	def base_json_ctrl(self, input_json):
		self.send_command(input_json)
