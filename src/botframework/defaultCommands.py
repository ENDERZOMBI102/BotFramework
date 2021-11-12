from . import logging

from discord import Message

from botframework import utils
from botframework.abc.server import AbstractServer
from botframework.commandSystem import Command
from botframework.dataclass.user import User


logger = logging.get_logger('defaultCommands')


def registerDefaults() -> None:
	logger.debug( 'Registering default commands' )

	@Command
	async def echo( server: AbstractServer, msg: Message ) -> None:
		""" sends the same message it received """
		echoed: str = msg.content.replace( 'echo ', '', 1 )
		if echoed == '':
			echoed = 'missing text!'
		await msg.channel.send( echoed )

	@Command
	async def hello( server: AbstractServer, msg: Message ) -> None:
		""" say hello to the author """
		await msg.channel.send( 'hello there!' )

	@Command
	async def pprefix( server: AbstractServer, msg: Message ) -> None:
		""" changes the personal prefix """
		prefix: str = msg.content[ 8: ].strip()
		if len( prefix ) > 4:
			await msg.channel.send( f'prefix too long! maximum length is 4.' )
		elif len( prefix ) == 0:
			await msg.channel.send( f'prefix too short! minimum length is 1.' )
		else:
			server.secondaryPrefix[ msg.author.id ] = prefix
			user: User = server.GetDatabase().getUser( msg.author.id )
			user.prefix = prefix
			server.GetDatabase().setUser( user )
			await msg.channel.send( f'personal prefix changed to "{prefix}"' )

	@Command
	async def savedata( server: AbstractServer, msg: Message ) -> None:
		if msg.author.id == utils.getAuthors()():
			server.GetDatabase().db.save()

	logger.info('Registered default commands')
