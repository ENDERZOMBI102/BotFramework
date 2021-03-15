from typing import Coroutine, Dict, Awaitable, Union

from discord import Message

from botframework import types
from botframework.abc.server import AbstractServer
from botframework.logging import get_logger

logger = get_logger()


class CommandSystem:

	__Commands: Dict[str, types.Coroutine] = {}

	def Command( self, func: Coroutine[ Awaitable[int], AbstractServer, Message ], cname: str = None ):
		"""
		The @decorator for commands
		:param func: coroutine to mark as command
		:param cname: usually None, used to set the command name
		"""
		func: types.Coroutine
		name = func.__code__.co_name.lower()
		logger.info(f'Registering command {name} from {func.__module__}')
		self.__Commands[ name if cname is None else cname ] = func
		return func

	def getOrDefault(
			self,
			item: str,
			default: Union[ Coroutine[ int, AbstractServer, Message ], types.Coroutine ]
	) -> Union[ Coroutine[ int, AbstractServer, Message ], types.Coroutine ]:
		"""
		Get the specified command or if not found, returns the one given on default
		:param item: the item to get
		:param default: fallback coroutine
		:return: the command or the default coroutine
		"""
		if item in self.__Commands.keys():
			return self.__Commands.get( item )
		else:
			return getattr( self, item, default )


instance: CommandSystem = CommandSystem()


def Command( func: Coroutine[ Awaitable[ int ], AbstractServer, Message ], cname: str = None ):
	"""
		The @decorator for commands
		:param func: coroutine to mark as command
		:param cname: usually None, used to set the command name
	"""
	return instance.Command(func, cname)


logger.debug( 'Registering default commands' )
from . import defaultCommands
logger.debug( 'Registered default commands' )
