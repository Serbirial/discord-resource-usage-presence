import threading
import subprocess
import time

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def get_model():
    line_as_bytes = subprocess.check_output("nvidia-smi -L", shell=True, startupinfo=startupinfo)
    line = line_as_bytes.decode("ascii")
    _, line = line.split(":", 1)
    line, _ = line.split("(")
    return line.strip()


class GpuWatcher:
	def __init__(self) -> None:
		self.running = True
		self.data = {
			"load": 0,

			"memory": 0,
			"memory_total": 0,

			"temperature": "0",
			"frequency": 0
		}

		self.thread = threading.Thread(target=self.data_loop)
		self.thread.start()

	def run_and_parse_ps1(self):
		p = subprocess.Popen(
			["powershell.exe", 
			"-ExecutionPolicy", "Bypass", 
			"-File", ".\\scripts\\windows\\gpu_information.ps1"], 
			stdout=subprocess.PIPE,
			startupinfo=startupinfo
			)
		
		keys, values = p.stdout.read().decode('utf-8').splitlines()
		values = values.split(",")

		table = {
			0: "load",
			1: "memory",
			2: "memory_total",
			3: "temperature",
			4: "frequency"
		}
		for x in range(5): # FIXME will error if ps1 file returns less or more than 5 CSV entries/whatever
			self.data[table[x]] = values[x]

	def data_loop(self):
		while self.running:
			self.run_and_parse_ps1()
			time.sleep(1.5)

	def return_data(self):
		return f"{self.data['load']} @ {self.data['frequency']} ({self.data['temperature'].strip()}C) VRAM @ {self.data['memory']} / {self.data['memory_total']}"
	
	def cleanup(self):
		self.running = False
		self.thread.join(0)