import threading
import psutil
import subprocess
import time

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def get_model():
	p = subprocess.Popen(
		["powershell.exe", 
		"-ExecutionPolicy", "Bypass", 
		"-File", ".\\windows\\cpu_name.ps1"], 
		stdout=subprocess.PIPE,
		startupinfo=startupinfo
		)
	return p.stdout.read().decode('utf-8').split(" ", 1)[1]

class CpuWatcher:
	def __init__(self) -> None:
		self.running = True
		self.load = 0
		self.frequency = 0
		self.cpu_count = psutil.cpu_count()
		self.thread = threading.Thread(target=self.data_loop)
		self.thread.start()

	def set_cpu_load(self):
		self.load = psutil.cpu_percent()

	def get_frequency(self):
		p = subprocess.Popen(
			["powershell.exe", 
			"-ExecutionPolicy", "Bypass", 
			"-File", ".\\windows\\cpu_frequency.ps1"], 
			stdout=subprocess.PIPE,
			startupinfo=startupinfo
			)
		frequency = p.stdout.read().decode('utf-8').split(".", 1)[0][:2]
		self.frequency = f"{frequency[:1]}.{frequency[1:]}"

	def data_loop(self):
		while self.running:
			self.set_cpu_load()
			self.get_frequency()
			time.sleep(1.5)

	def return_data(self):
		return f"CPU: {self.load}% ({self.frequency}Ghz)"
	
	def cleanup(self):
		self.running = False
		self.thread.join(0)