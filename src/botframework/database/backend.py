import sqlite3 as sql
from pathlib import Path
from typing import Any

from botframework.abc.database.backend import AbstractBackend
from botframework.logging import get_logger

logger = get_logger('database')


class SqlBackend(AbstractBackend):

	_dinstance: sql.Connection
	_cursor: sql.Cursor
	_dbpath: Path

	def __init__( self, path: str ) -> None:
		super(SqlBackend, self).__init__( path )
		self._dbpath = Path( path )
		self._dinstance = sql.connect( path )
		self._cursor = self._dinstance.cursor()
		# conditionally creates the tables
		self._cursor.execute(
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
		self._dinstance.commit()

	def makeRequest( self, sqlCode: str, *args: list[Any] ) -> list:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param sqlCode: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		self._cursor.execute( sqlCode, args )
		return self._cursor.fetchall()
