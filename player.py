from gameimage import GameImage
from tile import TILE_SIZE
from partymember import PartyMember
from inventory import Inventory
from equipment import WIZARD, PALADIN, NECROMANCER, WARRIOR, KNIGHT, BEASTMASTER, RANGER, DRUID, ROGUE
from gamescreen import LIGHT_BLUE
from spell import *
import pygame
from pygame import Surface, Rect, Color
import random

UP, DOWN, LEFT, RIGHT = "up", "down", "left", "right"
ENCOUNTER_MEAN, ENCOUNTER_SD = 700, 200

class Player(GameImage):
	def __init__(self, world):
		GameImage.__init__(self)
		self.party = []
		self.add_party_member(BERNARD)
		self.world_image = Surface((16, 16))
		self.rect = Rect(0, 0, 16, 16)
		self.world_image.fill(Color("#FF0000"))
		self.image = Surface((16, 16))
		self.image.blit(self.world_image, (0, 0))
		self.mask = pygame.mask.from_surface(self.image)
		self.world = world
		self.button_press_map = DEFAULT_BUTTON_PRESS_MAP
		self.summons = []
		self.xvel, self.yvel = 0, 0
		self.inventory = Inventory()
		self.reset_encounter_timer()
		self.totem_contact = False

	def update(self):
		self.xvel, self.yvel = 0, 0
		up, down, left, right = self.button_press_map[UP], self.button_press_map[DOWN], self.button_press_map[LEFT], self.button_press_map[RIGHT]
		if up and not down: self.yvel = -1
		if down and not up: self.yvel = 1
		if left and not right: self.xvel = -1
		if right and not left: self.xvel = 1
		self.rect.top += self.yvel
		self.rect.left += self.xvel
		tile = self.current_tile()
		self.check_entity_collisions(tile)
		#TODO: collision checks go here
		if self.xvel != 0 or self.yvel != 0: self.encounter_update(tile)

	def deactivate(self):
		self.button_press_map[UP], self.button_press_map[DOWN], self.button_press_map[LEFT], self.button_press_map[RIGHT] = False, False, False, False

	def add_party_member(self, key):
		spell_factory = SpellFactory()
		self.party.append(PartyMember(key, PARTY_MEMBER_MAP, spell_factory))

	def remove_summons(self):
		self.summons = []

	def encounter_update(self, tile):
		self.encounter_timer -= tile.base_encounter_rate
		if self.encounter_timer <= 0:
			monster_party = tile.roll_monster_party()
			self.begin_encounter(monster_party)
			self.reset_encounter_timer()

	def reset_encounter_timer(self):
		self.encounter_timer = random.gauss(ENCOUNTER_MEAN, ENCOUNTER_SD)

	def begin_encounter(self, monsters, battle_data = None):
		self.deactivate()
		self.world.screen_manager.switch_to_battle_screen(self, monsters, self.current_tile(), battle_data)

	def refresh_tile_flags(self):
		self.totem_contact = False

	def check_entity_collisions(self, tile):
		if tile.entity:
			self.refresh_mask()
			tile.entity.refresh_mask()
			if pygame.sprite.collide_rect(self, tile.entity): self.collide_with(tile.entity)
			else: self.refresh_tile_flags()
		else: self.refresh_tile_flags()

	def collide_with(self, entity):
		entity.take_effect(self)

	def begin_heal_flash(self):
		if self.totem_contact: return
		self.totem_contact = True
		self.world.begin_flash(LIGHT_BLUE, 100)

	def current_tile(self):
		x, y = self.rect.centerx/TILE_SIZE, self.rect.centery/TILE_SIZE
		return self.world.tile_at(x, y)

	def enqueue_action(self, index, key, target = None):
		if index >= len(self.party): actor = self.summons[index - len(self.party)]
		else: actor = self.party[index]
		actor.enqueue_action(key, target)

	def party_member_count(self):
		return len(self.party)

	def summon_count(self):
		return len(self.summons)

	def obtain_item(self, item):
		self.inventory.add_item(item)

class SpellFactory:
	def __init__(self):
		pass

	def generate_spell(self, key):
		return Spell(key)

DEFAULT_BUTTON_PRESS_MAP = {UP:False, DOWN:False, LEFT:False, RIGHT:False}

#attributes
NAME = "name"
PARTY_CLASS = "party_class"
HITPOINTS = "hitpoints"
MANA = "mana"
DAMAGE = "damage"
DEFENSE = "defense"
MAGIC_RESIST = "magic_resist"
SPEED = "speed"
MAGIC = "magic"
SPELLS = "spells"
LEVEL_UP_DATA = "level_up_data"

#party members
BERNARD = "bernard"
STEVEN = "steven"
OLIVER = "oliver"

PARTY_MEMBER_MAP = {
	BERNARD:{
		NAME:"Bernard",
		PARTY_CLASS:WIZARD,
		HITPOINTS:20,
		MANA:10,
		DAMAGE:1,
		DEFENSE:0,
		MAGIC_RESIST:2,
		SPEED:3,
		MAGIC:0,
		SPELLS:[SPARKS, SUMMON_GRASS_GOLEM, IVY_RAIN, SUMMON_WISP],
		LEVEL_UP_DATA:{
			2:{
				HITPOINTS:2,
				MANA:2,
				DAMAGE:1,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:1
			},
			3:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			4:{
				HITPOINTS:2,
				MANA:1,
				DAMAGE:1,
				DEFENSE:1,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:2				
			},
			5:{
				HITPOINTS:3,
				MANA:1,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:2,
				SPELLS:[THUNDERIDE]			
			},
			6:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			7:{
				HITPOINTS:2,
				MANA:1,
				DAMAGE:1,
				DEFENSE:1,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:0				
			},
			8:{
				HITPOINTS:2,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:0,
				MAGIC:2				
			},
			9:{
				HITPOINTS:3,
				MANA:1,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:1,
				MAGIC:1				
			},
			10:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:1,
				DEFENSE:1,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:2,
				SPELLS:[MULTISHOCK]				
			},
			11:{
				HITPOINTS:1,
				MANA:2,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:0				
			},
			12:{
				HITPOINTS:2,
				MANA:1,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:0,
				SPEED:0,
				MAGIC:0				
			},
			13:{
				HITPOINTS:3,
				MANA:0,
				DAMAGE:1,
				DEFENSE:2,
				MAGIC_RESIST:0,
				SPEED:0,
				MAGIC:0			
			},
			14:{
				HITPOINTS:2,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:2				
			},
			15:{
				HITPOINTS:3,
				MANA:5,
				DAMAGE:1,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:2,
				SPELLS:[GENTLE_TOUCH]	
			},
			16:{
				HITPOINTS:3,	#TEMP
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			17:{
				HITPOINTS:3,	#TEMP
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			18:{
				HITPOINTS:3,	#TEMP
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			19:{
				HITPOINTS:3,	#TEMP
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			20:{
				HITPOINTS:3,	#TEMP
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			}			
		}
	},
	STEVEN:{
		NAME:"Steven",
		PARTY_CLASS:WARRIOR,
		HITPOINTS:20,
		MANA:1,
		DAMAGE:2,
		DEFENSE:0,
		MAGIC_RESIST:-1,
		SPEED:4,
		MAGIC:0,
		SPELLS:[
		],
		LEVEL_UP_DATA:{		#ALL TEMP
			2:{
				HITPOINTS:2,
				MANA:2,
				DAMAGE:1,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:1
			},
			3:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			4:{
				HITPOINTS:2,
				MANA:1,
				DAMAGE:1,
				DEFENSE:1,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:2				
			},
			5:{
				HITPOINTS:3,
				MANA:1,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:2,
				SPELLS:[THUNDERIDE]			
			},
			6:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			7:{
				HITPOINTS:2,
				MANA:1,
				DAMAGE:1,
				DEFENSE:1,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:0				
			},
			8:{
				HITPOINTS:2,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:0,
				MAGIC:2				
			},
			9:{
				HITPOINTS:3,
				MANA:1,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:1,
				MAGIC:1				
			},
			10:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:1,
				DEFENSE:1,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:2,
				SPELLS:[MULTISHOCK]				
			},
			11:{
				HITPOINTS:1,
				MANA:2,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:0				
			},
			12:{
				HITPOINTS:2,
				MANA:1,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:0,
				SPEED:0,
				MAGIC:0				
			},
			13:{
				HITPOINTS:3,
				MANA:0,
				DAMAGE:1,
				DEFENSE:2,
				MAGIC_RESIST:0,
				SPEED:0,
				MAGIC:0			
			},
			14:{
				HITPOINTS:2,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:1,
				SPEED:0,
				MAGIC:2				
			},
			15:{
				HITPOINTS:3,
				MANA:5,
				DAMAGE:1,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:2,
				SPELLS:[GENTLE_TOUCH]	
			},
			16:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			17:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			18:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			19:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			},
			20:{
				HITPOINTS:3,
				MANA:3,
				DAMAGE:0,
				DEFENSE:0,
				MAGIC_RESIST:2,
				SPEED:1,
				MAGIC:1				
			}			
		}
	},
	OLIVER:{
		NAME:"Oliver",
		PARTY_CLASS:ROGUE,
		HITPOINTS:15,
		MANA:2,
		DAMAGE:4,
		DEFENSE:0,
		MAGIC_RESIST:0,
		SPEED:5,
		MAGIC:0,
		SPELLS:[
		]
	}
}