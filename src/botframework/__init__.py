from typing import Dict
import importlib

from discord import Client, Message, Reaction, Member

from .database.database import Database
from . import server
from . import utils
# import commandSystem, as it should be already up and running before the bot starts
from . import commandSystem
from .logging import get_logger
from .utils import embed, getColor
import modules

logger = get_logger( 'BOT' )


class Bot:
	instance: 'Bot'
	client: Client
	servers: Dict[ int, server.Server ] = {}
	database: Database

	def __init__( self ):
		Bot.instance = self
		self.client = Client()
		# register event listeners
		self.client.event( self.on_ready )
		self.client.event( self.on_message )
		self.database = Database()
		modules.initialize()

	def run( self, token: str ):
		""" Run the bot, its a blocking call """
		if token is None:
			raise ValueError('Passed None instead of the token!')
		self.client.run(token)

	def initLoggingAndRun( self, token: str, filename: str ):
		""" Initialize logging and run the bot, its a blocking call """
		if token is None:
			raise ValueError('Passed None instead of the token!')
		logging.init_logging( filename )
		self.client.run( token )

	async def on_ready( self ):
		"""	Called when the bot is ready to process incoming messages """
		logger.info( f'{self.client.user}: Ready.' )
		logger.info( f'The bot is currently in {len( self.client.guilds )} guilds.')

	async def on_reaction_add( self, reaction: Reaction, user: Member ):
		""" Called when an user reacts to a message """
		if reaction.message.author == self.client.user:
			return
		guild = reaction.message.guild.id
		await self.servers[ guild ].handleReactionAdd(reaction, user)

	async def on_reaction_remove( self, reaction: Reaction, user: Member ):
		""" Called when an user remove a reaction from a message """
		if reaction.message.author == self.client.user:
			return
		guild = reaction.message.guild.id
		await self.servers[ guild ].handleReactionRemove( reaction, user )

	async def on_message( self, msg: Message ):
		"""
		Called when a message arrives
		:param msg: the discord.Message obj
		"""

		if msg.author.bot:
			return

		from discord import TextChannel
		from discord import Guild
		msg.channel: TextChannel
		msg.guild: Guild
		# add the guild to the tracked server if it doesn't exist
		if msg.guild.id not in self.servers.keys():
			if msg.guild in self.client.guilds:
				logger.info( f'Got message from new guild "{msg.guild.name}", adding it!' )
				self.servers[ msg.guild.id ] = server.Server( msg.guild )
			else:
				logger.warning( f'Got message form unknown guild {msg.guild.name}, ignoring.' )
				return
		# don't permit to use echo to get permission elevation
		if msg.author == self.client.user:
			if 'echo' not in msg.content.split(' ')[0]:
				return
		# reloads the server instances and modules
		if msg.content == '$$reload' and msg.author.id == utils.getAuthors()():
			logger.warning(f'[RELOAD] reload issued in {msg.guild.name} by {msg.author.name}!')
			logger.info('[RELOAD] reloading!')
			await msg.channel.send('Reloading!')
			# clear all servers
			self.servers.clear()
			# reload modules
			import botframework.defaultCommands
			import modules
			try:
				# utils may be imported by the command system, reload it first
				importlib.reload( utils )
				# reload command system _BEFORE_ everything else
				importlib.reload( commandSystem )
				importlib.reload( botframework.defaultCommands )
				commandSystem.init()
				# reload the rest
				importlib.reload( server )
				modules.reload()
			except Exception as e:
				logger.error(f"[RELOAD] uncaught exception caught, can't complete reload!", exc_info=e)
				await msg.channel.send( embed=utils.getTracebackEmbed(e) )
			else:
				logger.info('[RELOAD] reload complete!')
				await msg.channel.send('Reloaded!')
		else:
			# call the right handler for the server
			await self.servers[ msg.guild.id ].handleMsg( msg )
