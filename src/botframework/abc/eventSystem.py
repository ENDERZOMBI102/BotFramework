from abc import ABCMeta, abstractmethod
from types import FunctionType

from botframework.types import Event


class AbstractEventSystem(metaclass=ABCMeta):

	@abstractmethod
	def removeListeners( self, module: str ):
		pass

	@abstractmethod
	def addListener( self, listener: FunctionType, event: Event ):
		pass
