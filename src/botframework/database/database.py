from typing import Any, Optional

from botframework.abc.database.backend import AbstractBackend
from botframework.abc.database.database import AbstractDatabase
from botframework.abc.database.guild import AbstractGuild
from botframework.database.backend import SqlBackend
from botframework.database.guild import Guild

_tables: dict[ str, list[str] ] = {
	'users': [
		'guildID',
		'discordID',
		'prefix'
	]
}


class Database(AbstractDatabase):

	_cache: dict[int, Guild] = {}
	instance: 'Database'
	_backend: AbstractBackend

	def __init__( self ) -> None:
		self._backend = SqlBackend( './resources/database.db' )
		Database.instance = self

	def getGuild( self, guild: int ) -> Optional[AbstractGuild]:
		"""
		Returns a Guild object for interacting with the database
		:param guild: guid ID
		:return: the Guild Object
		"""
		if guild not in self._cache.keys():
			self._cache[guild] = Guild(guild, self)
		return self._cache.get(guild)

	def makeRequest( self, sql: str, *args: Any, convertSingle: bool = True, table: str = '' ) -> list[ dict[str, Any] ]:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param convertSingle: def True, if True when a result list has a single item, extract it from the list and return it
		:param table: the table this request operates on
		:param sql: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		return _makeDictionary( table, self._backend.makeRequest( sql, *args ) )

	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		if self._backend is not None:
			self._backend.save()

	def __del__( self ) -> None:
		# save when closing!
		self.save()


def _makeDictionary( table: str, row: list[tuple] ) -> list[ dict[str, Any] ]:
	items: list[ dict[str, Any] ] = []
	for item in row:
		if table in _tables.keys():
			template = _tables[table]  # get the dictionary template from the known tables
			items.append(
				{
					# associate a key with a value
					template[pos]: value for pos, value in enumerate(item)
				}
			)
		else:
			items.append( { str(pos): value for pos, value in enumerate(item) } )

	return items
