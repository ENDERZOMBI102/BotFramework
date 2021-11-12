from discord import Client, Message, Reaction, Member

# import commandSystem, as it should be already up and running before the bot starts
from .logging import get_logger, init_logging
from . import eventSystem
from . import server
from . import commandSystem
from . import defaultCommands
from . import utils
from .database.database import Database
from .utils import embed, getColor

logger = get_logger( 'BOT' )


class Bot:
	instance: 'Bot'
	_client: Client
	_servers: dict[ int, server.Server ] = {}
	_database: Database

	def __init__( self, registerDefaultCommands: bool = False ) -> None:
		Bot.instance = self
		self._client = Client()
		# register event listeners
		self._client.event( self.on_ready )
		self._client.event( self.on_message )
		self._client.event( self.on_reaction_add )
		self._client.event( self.on_reaction_remove )
		# create db instance
		self._database = Database()
		# register default commands
		if registerDefaultCommands:
			defaultCommands.registerDefaults()

	def run( self, token: str ) -> None:
		""" Run the bot, its a blocking call """
		if token is None:
			raise ValueError('Passed None instead of the token!')
		self._client.run( token )

	def initLoggingAndRun( self, token: str, filename: str ) -> None:
		""" Initialize logging and run the bot, its a blocking call """
		if token is None:
			raise ValueError('Passed None instead of the token!')
		init_logging( filename )
		self._client.run( token )

	async def on_ready( self ) -> None:
		"""	Called when the bot is ready to process incoming messages """
		logger.info( f'{self._client.user}: Ready.' )
		logger.info( f'The bot is currently in {len( self._client.guilds )} guilds.' )

	async def on_reaction_add( self, reaction: Reaction, user: Member ) -> None:
		""" Called when an user reacts to a message """
		if reaction.message.author == self._client.user:
			return
		guild = reaction.message.guild.id
		await self._servers[ guild ].handleReactionAdd( reaction, user )

	async def on_reaction_remove( self, reaction: Reaction, user: Member ) -> None:
		""" Called when an user remove a reaction from a message """
		if reaction.message.author == self._client.user:
			return
		guild = reaction.message.guild.id
		await self._servers[ guild ].handleReactionRemove( reaction, user )

	async def on_message( self, msg: Message ) -> None:
		"""
		Called when a message arrives
		:param msg: the discord.Message obj
		"""

		# don't permit to use echo to get permission elevation
		# don't respond to other bots
		if msg.author.bot or msg.author == self._client.user:
			if 'echo' not in msg.content.split(' ')[0]:
				return

		# add the guild to the tracked server if it doesn't exist
		if msg.guild.id not in self._servers.keys():
			if msg.guild in self._client.guilds:
				logger.info( f'Got message from new guild "{msg.guild.name}", adding it!' )
				self._servers[ msg.guild.id ] = server.Server( msg.guild )
			else:
				logger.warning( f'Got message form unknown guild {msg.guild.name}, ignoring.' )
				return

		# reloads the server instances and modules
		if msg.content == '$$reload' and msg.author.id in utils.getAuthors()():
			logger.warning(f'[RELOAD] reload issued in {msg.guild.name} by {msg.author.name}!')
			logger.info('[RELOAD] reloading!')
			await msg.channel.send('Reloading!')
			# clear all servers
			self._servers.clear()
			# reload modules
			from . import moduleUtils
			try:
				# utils may be imported by the command system, reload it first
				moduleUtils.reload( utils )
				# reload event system _BEFORE_ everything else
				moduleUtils.reload( eventSystem )
				# then reload command system
				moduleUtils.reload( commandSystem )
				moduleUtils.reload( defaultCommands )
				# reload the rest
				moduleUtils.reload( server )
				await eventSystem.EventSystem.INSTANCE.invoke(eventSystem.Events.Reload)
			except Exception as e:
				logger.error(f"[RELOAD] uncaught exception caught, can't complete reload!", exc_info=e)
				await msg.channel.send( embed=utils.getTracebackEmbed(e) )
			else:
				logger.info('[RELOAD] reload complete!')
				await msg.channel.send('Reloaded!')
		else:
			# call the right handler for the server
			await self._servers[ msg.guild.id ].handleMsg( msg )
