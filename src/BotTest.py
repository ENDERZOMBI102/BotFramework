import os
from typing import List, Callable

import botframework


def getAuthors() -> Callable[ [], List[int] ]:
	return lambda: [ 350938367405457408 ]


botframework.utils.getAuthors = getAuthors  # security measure
botframework.server.defaultSecondaryPrefixes = { 350938367405457408: '$$' }  # set default secondary prefixes
botframework.Bot().initLoggingAndRun(
	token=os.environ.get( 'TOKEN' ),
	filename='../logs/latest.log'
)
