import pyinotify
import struct
import os

FILE_DIR = "/home/anshzinc/Documents/python/logdash/"
FILE_NAME = "test.txt"

class OnModifyEventHandler(pyinotify.ProcessEvent):
	def __init__(self, *args, **kwargs):
		super(OnModifyEventHandler, self).__init__(*args, **kwargs)

		self.file = open(FILE_DIR + FILE_NAME, 'r')
		st_results = os.stat(FILE_DIR + FILE_NAME)
		st_size = st_results[6]
		self.file.seek(st_size)

	def process_IN_MODIFY(self, event):
		if event.pathname == (FILE_DIR + FILE_NAME):
			print("[MODIFIED]:", event.pathname)
			self.print_lines()

	def print_lines(self):
		print(self.file.read())
		self.file.seek(0, 2)

def main():	
	event_handler = OnModifyEventHandler()

	wm = pyinotify.WatchManager()
	wm.add_watch(FILE_DIR, pyinotify.IN_MODIFY)

	notifier = pyinotify.Notifier(wm, event_handler)

	notifier.loop()


if __name__ == '__main__':
	main()

