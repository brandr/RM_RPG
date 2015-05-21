import pygame
from pygame import *
#from pygame import Surface, Color, Rect
import os

DEFAULT_COLORKEY = Color("#FF00FF")

def load_image_file(path, name, colorkey = DEFAULT_COLORKEY):
		""" load_image_file( str, str, str ) -> Surface

		Load an image from a filepath.
		"""
		fullname = os.path.join(path, name)
		try:
			image = pygame.image.load(fullname)
		except pygame.error, message:
			print 'Cannot load image:', name
			raise SystemExit, message
		image = image.convert()
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0, 0))
			image.set_colorkey(colorkey, RLEACCEL)
		return image

class GameImage(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
