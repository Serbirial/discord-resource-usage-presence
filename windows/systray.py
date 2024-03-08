import threading
import pystray
from PIL import Image

class SystemTray:
	def __init__(self, parent_object, tray_img_path) -> None:
		self.parent = parent_object

		self.menu = pystray.Menu(
			pystray.MenuItem("Exit", self.close_from_tray)
		)
		self.image = Image.open(tray_img_path)
		self.icon = pystray.Icon("Koya's Stats Presence", self.image, menu=self.menu)

		self.thread = threading.Thread(target=self.start)
		self.thread.start()

	def close(self):
		self.icon.stop()

	def close_from_tray(self, icon, query):
		print("Notifying main loop of close from tray...")
		self.parent.is_closing = True
		self.icon.stop()

	def start(self):
		print("Running SysTray")
		self.icon.run()