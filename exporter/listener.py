import pyinotify
import struct
import os
import asyncio

class OnModifyEventHandler(pyinotify.ProcessEvent):
	def __init__(self, exporter, file_path,parser,*args, **kwargs):
		super(OnModifyEventHandler, self).__init__(*args, **kwargs)

		self.exporter = exporter
		self.file_path = file_path
		self.parser = parser

		self.loop = asyncio.get_event_loop()
		
		self.new_line = ""
		self.file = open(file_path, 'r')

		st_results = os.stat(file_path)
		st_size = st_results[6]
		self.file.seek(st_size)

	def process_IN_MODIFY(self, event):
		if event.pathname == (self.file_path):
			print("[MODIFIED]:", event.pathname)
			self.print_lines()

	def print_lines(self):
		self.new_line = self.file.read()
		access_log_data = self.parser.parse(self.new_line)

		if access_log_data:
			self.loop.run_until_complete(self.exporter.send(access_log_data)) # send POST reqeust to server
		
		self.file.seek(0, 2)

def listen(exporter, file_path, parser):	
	event_handler = OnModifyEventHandler(exporter, file_path, parser)

	file_dir = os.path.dirname(file_path)
	wm = pyinotify.WatchManager()
	wm.add_watch(file_dir, pyinotify.IN_MODIFY)

	notifier = pyinotify.Notifier(wm, event_handler)

	notifier.loop()

