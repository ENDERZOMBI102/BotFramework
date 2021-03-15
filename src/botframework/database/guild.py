from typing import Dict, Any

from botframework.abc.database.database import AbstractDatabase
from botframework.abc.database.guild import AbstractGuild
from botframework.dataclass.user import User


class Guild(AbstractGuild):

	_userCache: Dict[str, User]

	def __init__(self, guildID: int, db: AbstractDatabase):
		super(Guild, self).__init__(guildID, db)
		self._userCache = {}

	def setUser( self, user: User ) -> None:
		"""
		Update the database by adding this user or by updating the saved user with this one
		:param user: an User object with new values
		"""
		if self.hasUser( user.discordID, checkCache=False ):
			self.db.makeRequest(
				# EXPLANATION: update an existing user
				'UPDATE users SET prefix = ? WHERE guildID = ? AND discordID = ?',
				# data
				user.prefix,
				# identification
				self.guildID,
				user.discordID
			)
		else:
			self.db.makeRequest(
				# EXPLANATION: insert a game with all their values
				'INSERT INTO users (guildID, discordID, prefix) VALUES (?, ?, ?)',
				# identification
				self.guildID,
				user.discordID,
				# data
				user.prefix
			)

	def getUser( self, discordID: int ) -> User:
		"""
		Gets a User from the user id
		:param discordID: the discord id of the user
		:return: the corresponding PapUser user
		"""
		if discordID not in self._userCache.keys():
			# EXPLANATION: select an user with userID userID and guildID of this guild
			userData: Dict[ str, Any ] = self.db.makeRequest(
				'SELECT * FROM users WHERE guildID = ? AND discordID = ?',
				self.guildID,
				discordID,
				table='users',
			)
			userData.pop( 'guildID' )
			self._userCache[ str( discordID ) ] = User( **userData )
		return self._userCache.get( str( discordID ) )

	def hasUser( self, discordID: int, checkCache: bool = True ) -> bool:
		"""
		Checks if has an user with that ID
		:param discordID: the user's discord id to check
		:param checkCache: True if should check the cache too
		:return: True if we have it
		"""
		if checkCache and discordID in self._userCache.keys():
			return True
		users: list = self.db.makeRequest(
			# EXPLANATION: select all users that are from this guild and their id is discordID
			'SELECT * FROM users WHERE guildID = ? AND discordID = ?',
			self.guildID,
			discordID
		)
		return len( users ) > 0
