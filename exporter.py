import os
import config
import listener
import parser
import asyncio
import aiohttp

from parsers.nginx_access_log_parser import NginxAccessLogParser


# Read config
WATCH_FILE = config.FILE_FULL_PATH
FILE_NAME = os.path.basename(WATCH_FILE)

LOGDASH_ADDR = config.LOGDASH_SERVER_ADDR

class Exporter:
	def __init__(self, listener, parser):
		self.listener = listener
		self.parser = parser

	def export(self):
		self.listener.listen(self, WATCH_FILE, self.parser)

	@asyncio.coroutine	
	def send(self, payload):
		url = LOGDASH_ADDR
		headers = {'content-type': 'application/json'}
	
		try:
			response = yield from aiohttp.request('post', url, data=payload, headers=headers) 		
			yield from response.release()
		except:
			print("Error sending data.")

if __name__ == '__main__':
	parser = NginxAccessLogParser()
	
	exporter = Exporter(listener, parser)
	exporter.export()

