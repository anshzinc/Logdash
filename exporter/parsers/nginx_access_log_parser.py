import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import base_parser
import re
import json

class NginxAccessLogParser(base_parser.Parser):
	def parse(self, line):
		pattern = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s' 	# IP address
           '\[(.+)\]\s' 				# datetime
           '"GET\s(.+)\s\w+/.+"\s\d+\s' # requested file
           '\d+\s"(.+)"\s' 				# referrer
           '"(.+)"' 					# user agent
        )
	
		match = re.findall(pattern, line)
		if match:
			data = json.dumps(match)
			return data
		
