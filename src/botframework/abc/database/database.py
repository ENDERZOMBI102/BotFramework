from abc import ABCMeta, abstractmethod
from typing import Any, Optional

from botframework.abc.database.guild import AbstractGuild
from botframework.database.backend import AbstractBackend


class AbstractDatabase(metaclass=ABCMeta):

	_backend: AbstractBackend

	@abstractmethod
	def getGuild( self, guild: int ) -> Optional['AbstractGuild']:
		"""
		Returns a Guild object for interacting with the database
		:param guild: guid ID
		:return: the Guild Object
		"""
		pass

	@abstractmethod
	def makeRequest( self, sql: str, *args: Any, convertSingle: bool = True, table: str = '' ) -> list[ dict[str, Any] ]:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param table: the table this request operates on
		:param convertSingle: def True, if True when a result list has a single item, extract it from the list and return it
		:param sql: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		pass

	@abstractmethod
	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		pass
