from types import FunctionType
from typing import Dict, Optional, Callable, cast

from botframework.logging import get_logger
from .types import CommandListener

logger = get_logger()


class CommandSystem:

	__Commands: Dict[ str, CommandListener ] = {}

	def Command( self, func: CommandListener, cname: Optional[str] ) -> CommandListener:
		"""
		The @decorator for commands
		:param func: coroutine to mark as command
		:param cname: usually None, used to set the command name
		"""
		name = func.__code__.co_name.lower()
		logger.info(f'Registering command {name} from {func.__module__}')
		self.__Commands[ cname or name ] = func
		return func

	def get( self, item: str ) -> Optional[CommandListener]:
		"""
		Get the specified command or if not found, returns the one given on default
		:param item: the item to get
		:return: the command or None
		"""
		if item in self.__Commands.keys():
			return self.__Commands.get( item )
		else:
			return None

	def getOrDefault( self, item: str, default: CommandListener ) -> CommandListener:
		"""
		Get the specified command or if not found, returns the one given on default
		:param item: the item to get
		:param default: fallback coroutine
		:return: the command or the default coroutine
		"""
		cmd = self.get(item)
		return cmd or default


instance: CommandSystem = CommandSystem()


def Command( *args: CommandListener | str, cname: str = None ) -> Callable[ [CommandListener], CommandListener ] | CommandListener:
	"""
		The @decorator for commands.
		this decorator may have a parameter: cname,
		cname is the command name to use instead of the decorated coroutine name.
	"""
	# check if called without parameters
	cname = cname or (
		(
				args[ 0 ].__name__[ 2 ].lower() + args[ 0 ].__name__[ 3: ]
		) if isinstance( args[ 0 ], FunctionType ) else cast( str, args[ 0 ] )
	)
	if len( args ) == 1 and isinstance( args[ 0 ], FunctionType ):
		return instance.Command( cast( CommandListener, args[0] ), None )

	# same as above, with wrapped in a lambda
	return lambda func: instance.Command(func, cname)
