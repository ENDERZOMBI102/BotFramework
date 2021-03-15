from botframework.abc.database.database import AbstractDatabase
from botframework.abc.database.guild import AbstractGuild
from botframework.dataclass.user import User


class Guild(AbstractGuild):

	def __init__(self, guildID: int, db: AbstractDatabase):
		super(Guild, self).__init__(guildID, db)

	def setUser( self, user: User ) -> None:
		pass

	def getUser( self, discordID: int ) -> User:
		pass

	def hasUser( self, discordID: int ) -> bool:
		pass
