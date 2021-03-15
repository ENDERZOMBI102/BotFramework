from enum import Enum
from typing import Dict, Union

from botframework.abc.eventSystem import AbstractEventSystem
from botframework.logging import get_logger
from botframework.types import ListenerList, Event, Coroutine

logger = get_logger('EventSystem')


class Events(Enum):
	ReactionAdded = 'add-react'
	ReactionRemoved = 'rem-react'
	MessageArrived = 'rec-msg'


class EventSystem(AbstractEventSystem):

	INSTANCE: 'EventSystem'
	_listeners: Dict[ Event, ListenerList ]

	def __init__(self):
		EventSystem.INSTANCE = self

	def removeListeners( self, module: str ):
		# cycle in all event lists
		for listenerList in self._listeners.values():
			toRemove = []
			for listener in listenerList:
				if listener.__module__ == module:
					toRemove.append( listener )  # schedule for removal all listeners of module module
			for func in toRemove:
				listenerList.remove(func)  # remove all found listeners

	def addListener( self, listener: Coroutine, event: Event ):
		# check if the event list exists
		if event not in self._listeners.keys():
			# if not, create it
			self._listeners[ event ] = [ ]
		# add the listener
		logger.info( f'Module "{listener.__module__}" registered listener for event "{event}".' )
		self._listeners[ event ].append( listener )

	async def invoke( self, event: Union[Event, Events], **kwargs ):
		"""
		Invoke an event, calling all listener that are listening for it, with the given kwargs.
		:param event: event to trigger
		:param kwargs: listener parameters
		:return:
		"""
		if event not in self._listeners.keys():
			self._listeners[ event ] = []

		if len( self._listeners[event ] ) == 0:
			logger.warning(f'Invoked event "{event}" has no _listeners!')

		for listener in self._listeners[event ]:
			try:
				await listener(**kwargs)
			except Exception as e:
				logger.error(
					f'Caught error for listener "{listener.__name__}" from module "{listener.__module__}" while invoking event {event}',
					exc_info=e
				)


# event listeners should be named:
# onEventName

def Listener(func: Coroutine):
	"""
	Decorator for event listeners.
	listeners should be named after the event they are listening for, ex:
	@Listener
	async def onMessage(server: AbstractServer, msg: Message):
		pass
	:param func: the listener
	"""
	event: str = func.__code__.co_name[2:].lower()
	# add the listener
	EventSystem.INSTANCE.addListener(func, event)
