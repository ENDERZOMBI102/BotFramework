import traceback
from typing import Any, List, Callable, Iterable
from random import choice

import discord
from discord import Embed, Color


def color_palette():
	"""
	Returns a random color from a Papaya fruit palette.
	:return: Random str("r,g,b") from papaya fruit palette
	"""
	colors = [
		"246,125,35",
		"253,150,58",
		"255,168,62",
		"186,163,49",
		"160,157,51"
	]
	return choice(colors)


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


def getColor(RGB: str = "255, 255, 255", random: bool = False) -> Color:
	"""
	Converts a string of R,G,B values to a discord Color object
	:param random:
	:param RGB: the color
	:return: color obj
	"""

	if random:
		rgb = color_palette().split(',')

	else:
		rgb = RGB.split(',')

	r: int = int( rgb[0] )
	g: int = int( rgb[1] )
	b: int = int( rgb[2] )
	returnColor = discord.colour.Color.from_rgb(r, g, b)

	return returnColor


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


def copyList(source: Iterable[Any] ) -> List[Any]:
	"""
	Copies an iterable to another list
	:param source: iterable to copy
	:return: the copied list
	"""
	return [ x for x in source]


def placeHolderFunc(*args, **kwargs):
	""" Just a placeholder for functions that require a function """
	return None


async def placeHolderCoro(*args, **kwargs):
	""" Just a placeholder for functions that require a coroutine """
	return None

