from gameimage import GameImage, load_image_file
from monster import Monster
from monsterparty import MonsterParty
from monsterfactory import generate_monster
from battledata import *
from player import STEVEN

class TileEntity(GameImage):
	def __init__(self, key):
		GameImage.__init__(self)
		filename = TILE_ENTITY_DATA_MAP[key][IMAGE_FILENAME]
		self.image = load_image_file("./images", filename)
		self.effect = TILE_ENTITY_DATA_MAP[key][EFFECT]
		self.key = key
		self.tile = None

	def take_effect(self, target):
		self.effect(self, target)

	def healing_totem_effect(self, target):	#TODO: add visual effect
		for p in target.party: 
			p.hitpoints[0] = p.hitpoints[1]
			p.mana[0] = p.mana[1]
		target.begin_heal_flash()

	def trigger_battle(self, target):
		data_map = TILE_ENTITY_DATA_MAP[self.key]
		monster_keys = data_map[MONSTERS]
		monsters = []
		for k in monster_keys: monsters.append(generate_monster(k))
		party = MonsterParty(monsters)
		#TODO: actually build the monsters as a list
		battle_data = BattleData(data_map[BATTLE_DATA])
		battle_data.delete_entity = self
		target.begin_encounter(party, battle_data)

	def delete(self):
		self.tile.clear_entity()

# attrbitues
IMAGE_FILENAME = "image_filenames"
EFFECT = "effect"
MONSTERS = "monsters"
BATTLE_DATA = "battle_data"

# tile entity types
HEALING_TOTEM = "healing_totem"
SVON = "svon"

TILE_ENTITY_DATA_MAP = {
	HEALING_TOTEM:{
		IMAGE_FILENAME:"healing_totem_1.bmp",
		EFFECT:TileEntity.healing_totem_effect
	},
	SVON:{	# triggers a battle with SVON
		IMAGE_FILENAME:"world_svon_1.bmp",
		EFFECT:TileEntity.trigger_battle,
		MONSTERS:[SVON],
		BATTLE_DATA:{
			POST_BATTLE_EVENT:[
				(TEXT, "Steven joined your party!"),
				(PARTY_MEMBER_JOIN, STEVEN)
			]
		}
	}
}