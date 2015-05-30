import random

class Spell:
	def __init__(self, key):
		self.key = key

	def name(self):
		return SPELL_DATA_MAP[self.key][NAME]

	def mp_cost(self):
		return SPELL_DATA_MAP[self.key][MP_COST]

	def spell_type(self):
		return SPELL_DATA_MAP[self.key][SPELL_TYPE]

	def targeting(self):
		return SPELL_DATA_MAP[self.key][TARGETING]

	def execute_action(self, screen):
		if self.targeting() == MULTIPLE and self.spell_type() == ATTACK:
			target = self.targets[self.target_index]
			damage = self.roll_damage(self.caster, target)
			screen.misc_message = self.name() + " hit " + target.battle_name + " for " + str(damage) + " damage!"
			target.take_damage(damage)
			if target.hitpoints[0] > 0: self.target_index += 1

	def cast(self, caster, screen):
		self.caster = caster
		spell_map = SPELL_DATA_MAP[self.key]
		if caster.mana[0] < spell_map[MP_COST]:
			self.spell_fail(caster, screen)
			return
		targeting, spell_type = spell_map[TARGETING], spell_map[SPELL_TYPE]
		method = CAST_MAP[spell_type][targeting]
		method(self, caster, screen)
		caster.lose_mp(self.mp_cost())

	def roll_damage(self, caster, target):
		base_attack = SPELL_DATA_MAP[self.key][DAMAGE] + caster.magic #TODO: calculate differently as spells get more complex 
		offset = max(1, base_attack/5.0)
		damage = max(1, random.randint(round(base_attack - offset), round(base_attack + offset)))
		damage = max(0, damage - target.armor_value())
		return damage

	def cast_single_attack(self, caster, screen):
		target = caster.pending_target
		damage = self.roll_damage(caster, target)
		screen.misc_message = caster.name + " cast " + self.name() + " at " + target.name + " for " + str(damage) + " damage!"
		target.take_damage(damage)

	def cast_multiple_attack(self, caster, screen):
		targets = screen.monsters.monsters
		self.targets = targets
		self.target_index = 0
		screen.enqueue_spell_set(self, targets)
		screen.misc_message = caster.name + " cast " + self.name() + "!"

	def cast_summon(self, caster, screen):
		summon_map = SPELL_DATA_MAP[self.key][SUMMON_DATA]
		screen.misc_message = caster.name + " summoned " + summon_map[NAME] + "!"
		creature = Summon(summon_map)
		screen.player.summons.append(creature)

	def spell_fail(self, caster, screen):
		screen.misc_message = caster.name + " tried to cast " + self.name() + ", but failed!"

from partymember import PartyMember

class Summon(PartyMember):
	def __init__(self, data_map):
		PartyMember.__init__(self)
		self.name = data_map[NAME]
		hitpoints = data_map[HITPOINTS]
		self.hitpoints = [hitpoints, hitpoints]	#TEMP
		mana = data_map[MANA]
		self.mana = [mana, mana]
		spells = data_map[SPELLS]
		self.spells = []
		for key in spells: self.spells.append(Spell(key))
		self.attack_stat = data_map[DAMAGE]
		self.defense = data_map[DEFENSE]
		self.speed = data_map[SPEED]
		self.magic = data_map[MAGIC]
		self.pending_action = None
		self.pending_target = None
		self.pending_spell = None

	def weapon_damage(self):
		return 0

	def armor_value(self):
		return 0
		#return self.defense

# attributes
NAME = "name"
TARGETING = "targeting"
SPELL_TYPE = "spell_type"
MP_COST = "mp_cost"
TARGETING = "targeting"
DAMAGE = "damage"
SUMMON_DATA = "summon_data"

# targeting styles
SINGLE = "single"
MULTIPLE = "multiple"

# spell types
ATTACK = "attack"
SUMMON = "summon"

# summon data
HITPOINTS = "hitpoints"
MANA = "mana"
SPEED = "speed"
MAGIC = "magic"
DEFENSE = "defense"
SPELLS = "spells"

# spells
FIRE = "fire"
SPARKS = "sparks"
SUMMON_GRASS_GOLEM = "summon_grass_golem"
GRASS_ENTANGLEMENT = "grass_entanglement"
IVY_RAIN = "ivy_rain"

CAST_MAP = {
	ATTACK:{
		SINGLE:Spell.cast_single_attack,
		MULTIPLE:Spell.cast_multiple_attack
	},
	SUMMON:{
		SINGLE:Spell.cast_summon
	}
}

SPELL_DATA_MAP = {
	FIRE:{
		NAME:"Fire",
		TARGETING:SINGLE,
		SPELL_TYPE:ATTACK,
		MP_COST:2,
		DAMAGE:5
	},
	SPARKS:{
		NAME:"Sparks",
		TARGETING:SINGLE,
		SPELL_TYPE:ATTACK,
		MP_COST:1,
		DAMAGE:5
	},
	SUMMON_GRASS_GOLEM:{
		NAME:"Summon Grass Golem",
		TARGETING:SINGLE,
		SPELL_TYPE:SUMMON,
		MP_COST:6,
		SUMMON_DATA:{
			NAME:"G. Golem",
			HITPOINTS:15,
			MANA:2,
			DAMAGE:3,
			MAGIC:0,
			DEFENSE:0,
			SPEED:1,
			SPELLS:[
				GRASS_ENTANGLEMENT
			]
		}
	},
	GRASS_ENTANGLEMENT:{
		NAME:"Grass Entanglement",
		TARGETING:SINGLE,
		SPELL_TYPE:ATTACK,
		MP_COST:2,
		DAMAGE:2
		#TODO: lasting effect: enemies hit by grass entanglement cannot move next turn
	},
	IVY_RAIN:{
		NAME:"Ivy Rain",
		TARGETING:MULTIPLE,
		SPELL_TYPE:ATTACK,
		MP_COST:3,
		DAMAGE:2
	}
}

