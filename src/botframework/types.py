from types import CodeType
from typing import Awaitable, Protocol, Any

from discord import Message

from botframework.abc.server import AbstractServer

Event = str


class EventListener(Protocol):
	__code__: CodeType
	__name__: str
	__module__: str

	def __call__( self, *args: Any, **kwargs: Any ) -> Awaitable[None]:
		pass


EventListenerList = list[EventListener]


class CommandListener(Protocol):
	__code__: CodeType
	__name__: str
	__module__: str

	def __call__(self, server: AbstractServer, msg: Message) -> Awaitable[None]:
		pass
