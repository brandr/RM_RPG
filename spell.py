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

	def cast(self, caster, screen):
		spell_map = SPELL_DATA_MAP[self.key]
		if caster.mana[0] < spell_map[MP_COST]:
			self.spell_fail(caster, screen)
			return
		targeting, spell_type = spell_map[TARGETING], spell_map[SPELL_TYPE]
		method = CAST_MAP[spell_type][targeting]
		method(self, caster, screen)
		caster.lose_mp(self.mp_cost())

	def roll_damage(self, target):
		base_attack = SPELL_DATA_MAP[self.key][DAMAGE] #TODO: calculate differently as spells get more complex are added
		offset = max(1, base_attack/5.0)
		return max(1, random.randint(round(base_attack - offset), round(base_attack + offset)))

	def cast_single_attack(self, caster, screen):
		damage = self.roll_damage(caster.pending_target)
		screen.misc_message = caster.name + " cast " + self.name() + " at " + caster.pending_target.name + " for " + str(damage) + " damage!"
		caster.pending_target.take_damage(damage)

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
		self.speed = data_map[SPEED]
		self.pending_action = None
		self.pending_target = None
		self.pending_spell = None

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
MISC = "misc"

# spell types
ATTACK = "attack"
SUMMON = "summon"

# summon data
HITPOINTS = "hitpoints"
MANA = "mana"
SPEED = "speed"
SPELLS = "spells"

# spells
FIRE = "fire"
SPARKS = "sparks"
SUMMON_GRASS_GOLEM = "summon_grass_golem"
GRASS_ENTANGLEMENT = "grass_entanglement"

CAST_MAP = {
	ATTACK:{
		SINGLE:Spell.cast_single_attack
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
	}
}
