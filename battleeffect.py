class BattleEffect:
	def __init__(self, key, arg):
		self.key = key
		init_method = EFFECT_MAP[key][INIT]
		init_method(self, arg)

	def decrement_duration(self, target):
		self.duration -= 1
		if self.duration <= 0: target.active_effects.remove(self)

	def init_stun(self, duration):
		self.duration = duration

	def execute_stun(self):
		pass #not needed


# effect constants
INIT = "init"
EXECUTE = "execute"

# effect types
STUN = "stun"

EFFECT_MAP = {
	STUN:{
		INIT:BattleEffect.init_stun,
		EXECUTE:BattleEffect.execute_stun
	}
}