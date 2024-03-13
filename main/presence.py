from pypresence import Presence
from pypresence.exceptions import PipeClosed

class Connection:
	def __init__(self) -> None:
		self.client_id = '1215333269273579621'
		self.connect()

	def connect(self):
		self.rpc = Presence(self.client_id, pipe=0) 
		self.rpc.connect()

	def update(self, cpu, memory, gpu, models):
		try:
			self.rpc.update(
				details=cpu,
				state=memory,

				large_image="pc_orange",
				large_text=models,

				small_image="nvidia",
				small_text=gpu
			)
		except PipeClosed:
			self.connect()