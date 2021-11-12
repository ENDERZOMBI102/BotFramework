from collections import defaultdict
from enum import Enum
from types import FunctionType
from typing import Callable, cast, Any

from botframework.abc.eventSystem import AbstractEventSystem
from botframework.logging import get_logger
from botframework.types import EventListenerList, Event, EventListener

logger = get_logger('EventSystem')


class Events(Enum):
	ReactionAdded = 'ReactionAdded'.lower()
	ReactionRemoved = 'ReactionRemoved'.lower()
	MessageArrived = 'message'
	Reload = 'reload'


class EventSystem(AbstractEventSystem):

	INSTANCE: 'EventSystem'
	_listeners: dict[ Event | Events, EventListenerList ]

	def __init__(self) -> None:
		EventSystem.INSTANCE = self
		self._listeners = defaultdict( lambda: [] )

	def removeListeners( self, module: str ) -> None:
		# cycle in all event lists
		for listenerList in self._listeners.values():
			toRemove = []
			for listener in listenerList:
				if listener.__module__ == module:
					toRemove.append( listener )  # schedule for removal all listeners of module module
			for func in toRemove:
				listenerList.remove(func)  # remove all found listeners

	def addListener( self, listener: EventListener, event: Event ) -> EventListener:
		# add the listener
		logger.info( f'Module "{listener.__module__}" registered listener for event "{event}".' )
		self._listeners[ event ].append( listener )
		return listener

	async def invoke( self, event: Event | Events, **kwargs: Any ) -> None:
		"""
		Invoke an event, calling all listeners that are listening for it, with the given kwargs.
		:param event: event to trigger
		:param kwargs: listener parameters
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


EventSystem()


# event listeners should be named:
# onEventName

def Listener( *args: str | EventListener, event: str = None ) -> Callable[ [EventListener], EventListener ] | EventListener:
	"""
	Decorator for event listeners.
	listeners should be named after the event they are listening for, ex:

	@Listener
	async def onMessage(server: AbstractServer, msg: Message):
		pass

	if this is not possible, an event parameter can be passed to the decorator to set it,
	"""
	event = event or (
		(
			args[ 0 ].__name__[ 2 ].lower() + args[ 0 ].__name__[ 3: ]
		) if isinstance( args[ 0 ], FunctionType ) else cast( str, args[ 0 ] )
	)

	if len( args ) == 1 and isinstance( args[ 0 ], FunctionType ):
		# called with no arguments
		return EventSystem.INSTANCE.addListener( cast( FunctionType, args[ 0 ] ), cast( str, event ) )

	# called with arguments
	def wrapper(func: EventListener) -> EventListener:
		return EventSystem.INSTANCE.addListener( func, cast( str, event ) )

	return wrapper
