import os

import botframework


botframework.utils.getAuthors = lambda: lambda: [ 350938367405457408 ]  # security measure
botframework.server.defaultSecondaryPrefixes = { 350938367405457408: '$$' }  # set default secondary prefixes
botframework.Bot(registerDefaultCommands=True).initLoggingAndRun(
	token=os.environ.get( 'TOKEN' ),
	filename='../logs/latest.log'
)
