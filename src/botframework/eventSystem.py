from typing import Dict, List

from botframework.logging import get_logger
from botframework.types import ListenerList, Event, Coroutine

logger = get_logger('EventSystem')


class EventSystem:

	INSTANCE: 'EventSystem'
	listeners: Dict[Event, ListenerList]

	def __init__(self):
		EventSystem.INSTANCE = self

	def removeListener( self, module: str ):
		# cycle in all event lists
		for listenerList in self.listeners.values():
			toRemove = []
			for listener in listenerList:
				if listener.__module__ == module:
					toRemove.append( listener )  # schedule for removal all listeners of module module
			for func in toRemove:
				listenerList.remove(func)  # remove all found listeners

	def addListener( self, listener: Coroutine, event: Event ):
		# check if the event list exists
		if event not in self.listeners.keys():
			# if not, create it
			self.listeners[ event ] = [ ]
		# add the listener
		self.listeners[ event ].append( listener )

	async def invoke( self, event: Event, **kwargs ):
		if event not in self.listeners.keys():
			self.listeners[ event ] = []

		if len( self.listeners[event] ) == 0:
			logger.warning(f'Invoked event "{event}" has no listeners!')

		for listener in self.listeners[event]:
			await listener(**kwargs)


# event listeners should be named:
# onEventName

def Listen(func: Coroutine):
	event: str = func.__code__.co_name[2:].lower()
	# add the listener
	EventSystem.INSTANCE.addListener(func, event)
