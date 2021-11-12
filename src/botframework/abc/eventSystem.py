from abc import ABCMeta, abstractmethod

from botframework.types import Event, EventListener


class AbstractEventSystem(metaclass=ABCMeta):

	@abstractmethod
	def removeListeners( self, module: str ) -> None:
		pass

	@abstractmethod
	def addListener( self, listener: EventListener, event: Event ) -> EventListener:
		pass
