import os

import botframework


botframework.Bot().initLoggingAndRun(
	token=os.environ.get( 'TOKEN' ),
	filename='../logs/latest.log'
)
