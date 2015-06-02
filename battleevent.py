class BattleEvent:

	def __init__(self, key, arg):
		self.key = key
		init_method = BATTLE_EVENT_MAP[key][INIT]
		init_method(self, arg)

	def execute(self, screen):
		execute_method = BATTLE_EVENT_MAP[self.key][EXECUTE]
		execute_method(self, screen)

	def init_text(self, text):
		self.text = text

	def init_party_member_join(self, party_key):
		self.party_key = party_key

	def execute_text(self, screen):
		screen.misc_message = self.text

	def execute_party_member_join(self, screen):
		screen.player.add_party_member(self.party_key)

INIT = "init"
EXECUTE = "execute"

#battle event types
TEXT = "text"
PARTY_MEMBER_JOIN = "party_member_join" 

BATTLE_EVENT_MAP = {
	TEXT:{
		INIT:BattleEvent.init_text,
		EXECUTE:BattleEvent.execute_text
	},
	PARTY_MEMBER_JOIN:{
		INIT:BattleEvent.init_party_member_join,
		EXECUTE:BattleEvent.execute_party_member_join
	}
}