from abc import ABCMeta, abstractmethod

from botframework.abc.database.database import AbstractDatabase
from botframework.dataclass.user import User


class AbstractGuild(metaclass=ABCMeta):

	guildID: int
	db: AbstractDatabase

	def __init__(self, guildID: int, db: AbstractDatabase):
		self.guildID = guildID
		self.db = db

	@abstractmethod
	def getUser( self, discordID: int ) -> User:
		pass

	@abstractmethod
	def setUser( self, user: User ) -> None:
		pass

	@abstractmethod
	def hasUser( self, discordID: int ) -> bool:
		pass

