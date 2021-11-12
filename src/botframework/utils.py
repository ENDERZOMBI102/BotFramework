import traceback
from typing import TypeVar, List, Callable, Iterable, Any
from random import choice

import discord
from discord import Embed, Color


T = TypeVar('T')


def getAuthors() -> Callable[ [], List[int] ]:
	return lambda: []


def embed(title: str, content: str, color: Color) -> Embed:
	"""
	Creates an embed from its data
	:param title: title of the embed
	:param content: the content of the embed, only text
	:param color: the color of the line of the embed
	:return: the embed
	"""
	data = Embed(
		color=color,
		title=title,
		description=content,
		type='rich_embed'
	)
	return data


def getColor(RGB: str = '255, 255, 255') -> Color:
	"""
	Converts a string of R,G,B values to a discord Color object
	:param RGB: the color
	:return: color obj
	"""
	r, g, b = RGB.split(',')
	return discord.colour.Color.from_rgb( int( r ), int( g ), int( b ) )


def getTracebackEmbed( exc: Exception ) -> Embed:
	"""
	Create an embed from an exception object
	:param exc: the exception to transform
	:return: the final Embed
	"""
	prettyExc = ''.join( traceback.format_exception( type( exc ), exc, exc.__traceback__ ) )
	print( prettyExc )
	return embed(
		title='Uncaught Exception!',
		content=prettyExc,
		color=discord.Color.red()
	)


def copyList(source: Iterable[T] ) -> List[T]:
	"""
	Copies an iterable to another list
	:param source: iterable to copy
	:return: the copied list
	"""
	return [ x for x in source]


def placeHolderFunc(*args: Any, **kwargs: Any) -> None:
	""" Just a placeholder for functions that require a function """
	return None


async def placeHolderCoro(*args: Any, **kwargs: Any) -> None:
	""" Just a placeholder for functions that require a coroutine """
	return None

