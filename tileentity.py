from gameimage import GameImage, load_image_file

class TileEntity(GameImage):
	def __init__(self, key):
		GameImage.__init__(self)
		filename = TILE_ENTITY_DATA_MAP[key][IMAGE_FILENAME]
		self.image = load_image_file("./images", filename)
		self.effect = TILE_ENTITY_DATA_MAP[key][EFFECT]

	def take_effect(self, target):
		self.effect(self, target)

	def healing_totem_effect(self, target):	#TODO: add visual effect
		for p in target.party: 
			p.hitpoints[0] = p.hitpoints[1]
			p.mana[0] = p.mana[1]
		target.begin_heal_flash()

# attrbitues
IMAGE_FILENAME = "image_filenames"
EFFECT = "effect"

# tile entity types
HEALING_TOTEM = "healing_totem"

TILE_ENTITY_DATA_MAP = {
	HEALING_TOTEM:{
		IMAGE_FILENAME:"healing_totem_1.bmp",
		EFFECT:TileEntity.healing_totem_effect
	}
}