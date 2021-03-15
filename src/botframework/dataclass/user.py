class User:

	discordID: int
	prefix: str

	def __init__(self, discordID: int, prefix: str):
		self.discordID = discordID
		self.prefix = prefix
