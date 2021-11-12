from abc import ABCMeta, abstractmethod

import discord

from botframework.abc.database.guild import AbstractGuild


class AbstractServer(metaclass=ABCMeta):

	guild: discord.Guild
	prefix: str = '!!'
	roleRules: dict[ str, object ]
	secondaryPrefix: dict[int, str]

	@abstractmethod
	async def handleMsg( self, msg: discord.Message ) -> None:
		"""
		Handles a discord message object
		:param msg: message to handle
		"""
		pass

	@abstractmethod
	async def handleReactionAdd( self, reaction: discord.Reaction, user: discord.Member ) -> None:
		"""
		Handles reacting to a message with an emoji
		:param reaction: the reaction object
		:param user: the user who caused this event
		"""

	@abstractmethod
	async def handleReactionRemove( self, reaction: discord.Reaction, user: discord.Member ) -> None:
		"""
		Handles removing a reaction to a message
		:param reaction: the reaction object
		:param user: the user who caused this event
		"""

	@abstractmethod
	def GetDatabase( self ) -> AbstractGuild:
		"""
		Getter for this guild's database interface
		:return: Database object
		"""
		pass
