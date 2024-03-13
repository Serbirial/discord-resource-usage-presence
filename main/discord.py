from windows import (
	cpu,
	gpu,
	memory,
	systray
)
import time

from sys import exit
from json import loads

from .presence import Connection


try:
	with open("config.json", "r") as data:
		CONFIG = loads(data.read())
except FileNotFoundError:
	CONFIG = {
		"interval": 5,
		"tray_icon": "static/tray.png",
		"exe": False
		}

CPU_MODEL = cpu.get_model()
GPU_MODEL = gpu.get_model()
MODEL_STRING = f"{CPU_MODEL}\n{GPU_MODEL}"

ITERATE_MODELS = False

if len(MODEL_STRING) >= 128:
	print("Switching between models because models string is more than 128 characters...")
	ITERATE_MODELS = True


class DiscordPcStatus:
	def __init__(self) -> None:
		self.is_closing = False

		self.tray = systray.SystemTray(self, CONFIG["tray_icon"])

		self.discord_connection = Connection()

		self.cpustats = cpu.CpuWatcher()
		self.gpustats = gpu.GpuWatcher()

		self.memstats = memory.MemoryWatcher()
		self.current_model = CPU_MODEL

	def cleanup(self):
		print("Cleaning up...")
		self.tray.close()
		self.cpustats.cleanup()
		self.gpustats.cleanup()
		self.memstats.cleanup()
		print("Exiting...")
		try:
			exit() # FIXME causes issues with windows exe
		except:
			pass

	def start(self):
		current_model = CPU_MODEL
		while not self.is_closing:
			self.discord_connection.update(
				cpu=self.cpustats.return_data(),
				memory=self.memstats.return_data(),
				gpu=self.gpustats.return_data(),
				models=MODEL_STRING if not ITERATE_MODELS else current_model 
			)
			if ITERATE_MODELS:
				if current_model == CPU_MODEL:
					current_model = GPU_MODEL
				elif current_model == GPU_MODEL:
					current_model = CPU_MODEL

			time.sleep(CONFIG['interval'])
		self.cleanup()
