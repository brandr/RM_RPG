from battleevent import *

class BattleData:

	def __init__(self, data_map):
		if PRE_BATTLE_EVENT in data_map: self.init_pre_battle_event(data_map[PRE_BATTLE_EVENT])
		if POST_BATTLE_EVENT in data_map: self.init_post_battle_event(data_map[POST_BATTLE_EVENT])
		self.pre_index, self.post_index = 0, 0
		self.mode = None
		self.delete_entity = None

	def post_update(self, screen):
		if not self.post_battle_events: return False
		if self.mode != POST_BATTLE_EVENT:
			self.mode = POST_BATTLE_EVENT
			return True
		if self.post_index < len(self.post_battle_events):
			self.post_battle_events[self.post_index].execute(screen)
			self.post_index += 1
			return True
		self.delete_connected_entity()
		return False

	def init_pre_battle_event(self, data_list):
		self.pre_battle_events = []
		for d in data_list:
			event = BattleEvent(d[0], d[1])
			self.pre_battle_events.append(event)

	def init_post_battle_event(self, data_list):
		self.post_battle_events = []
		for d in data_list:
			event = BattleEvent(d[0], d[1])
			self.post_battle_events.append(event)

	def delete_connected_entity(self):
		if self.delete_entity: self.delete_entity.delete()

PRE_BATTLE_EVENT = "pre_battle_event"
POST_BATTLE_EVENT = "post_battle_event"