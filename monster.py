from gameimage import GameImage

class Monster(GameImage):
	def __init__(self, key):
		GameImage.__init__(self)
		self.key = key