import sqlite3 as sql
from pathlib import Path
from typing import List, Any

from botframework.abc.database.backend import AbstractBackend
from botframework.logging import get_logger

logger = get_logger('database')


class SqlBackend(AbstractBackend):

	dinstance: sql.Connection
	cursor: sql.Cursor
	dbpath: Path

	def __init__( self, path: str = None ):
		super(SqlBackend, self).__init__( path )
		self.dbpath = Path(path)
		self.dinstance = sql.connect(path)
		self.cursor = self.dinstance.cursor()
		# conditionally creates the tables
		self.cursor.execute(
			'''
			CREATE TABLE IF NOT EXISTS users (
				guildID INTEGER NOT NULL,
				discordID INTEGER NOT NULL,
				prefix TEXT NOT NULL DEFAULT '!',
				CONSTRAINT PK_user PRIMARY KEY (guildID, discordID)
			)
			'''
		)

	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		self.dinstance.commit()

	def makeRequest( self, sqlCode: str, *args: List[Any] ) -> Any:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param sqlCode: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		self.cursor.execute( sqlCode, args )
		return self.cursor.fetchall()
