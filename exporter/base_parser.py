import abc

class Parser(metaclass = abc.ABCMeta):
	
	@abc.abstractmethod
	def parse(self):
		return	
