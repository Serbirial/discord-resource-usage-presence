import threading
import psutil
import time


class MemoryWatcher:
	def __init__(self) -> None:
		self.running = True
		self.usage = 0
		self.total = psutil.virtual_memory().total >> 20
		self.thread = threading.Thread(target=self.data_loop)
		self.thread.start()


	def set_memory_usage(self):
		self.usage = psutil.virtual_memory().used >> 20

	def data_loop(self):
		while self.running:
			self.set_memory_usage()
			time.sleep(1.5)

	def return_data(self):
		usage = f"{self.usage:,}".split(",", 1)[0]
		total = f"{self.total:,}".split(",", 1)[0]
		return f"RAM: {usage} / {total} GB used."
	
	def cleanup(self):
		self.running = False
		self.thread.join(0)