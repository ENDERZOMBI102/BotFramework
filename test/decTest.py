from types import FunctionType
from typing import Callable


class Decorator:

	message: str

	def __init__( self, *args: str | FunctionType | None, msg: str = None ):
		self.message = msg or (
			args[0].__name__[2].lower() + args[0].__name__[3:] if isinstance( args[0], FunctionType ) else args[0]
		)
		if len(args) > 0 and isinstance( args[0], FunctionType ):
			print( f'__init__(): {args[0]} - {self.message}' )

	def __call__(self, listener: Callable):
		print( f'__call__(): {listener} - {self.message}' )


@Decorator( 'exactly' )
def func() -> None:
	pass


@Decorator( msg='exactly' )
def func() -> None:
	pass


@Decorator
def onExactly() -> None:
	pass


