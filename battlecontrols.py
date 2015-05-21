from controls import *

ACTION_COUNT = 4

class BattleControls(Controls):
	""" MapControls( Player ) -> MapControls

	The inventory controls are used to make item-based changes or to exit the inventory screen.

	Attributes:

	player: The Player whose inventory is controlled via these controls.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(BATTLE_CONTROL_MAP)
		self.player = player
		#self.battle_state = SELECT_ACTION

	def unpause(self, key, toggle):
		""" mc.unpause( str, bool ) -> None

		When the player presses enter, resume the game.
		"""
		if toggle: self.player.unpause_game()

	def press_enter(self, key, toggle):
		if not toggle: return
		if not self.battle_state() in BATTLE_ENTER_MAP: return
		action = BATTLE_ENTER_MAP[self.battle_state()]
		action(self)

	def press_escape(self, key, toggle):
		if not toggle: return
		if not self.battle_state() in BATTLE_ESCAPE_MAP: return
		action = BATTLE_ESCAPE_MAP[self.battle_state()]
		action(self)

	def move_cursor(self, key, toggle):
		""" mc.move_cursor( str, bool ) -> None

		Move the inventory cursor from its current position to select an item.
		"""
		if not toggle: return
		if not self.battle_state() in BATTLE_MOVE_CURSOR_MAP: return
		action = BATTLE_MOVE_CURSOR_MAP[self.battle_state()]
		action(self, key)

	def return_to_action_select(self):
		self.control_manager.screen.mode = SELECT_ACTION

	def move_action_cursor(self, key):
		direction = DIRECTION_MAP[key] 
		self.control_manager.screen.action_index = ( self.control_manager.screen.action_index + direction[1] ) % ACTION_COUNT

	def move_target_cursor(self, key):
		screen = self.control_manager.screen
		direction = DIRECTION_MAP[key]
		target_count = screen.target_count()
		screen.target_index = ( screen.target_index + direction[0] ) % target_count

	def move_item_cursor(self, key):
		screen = self.control_manager.screen
		direction = DIRECTION_MAP[key]
		item_count = screen.item_count()
		screen.item_select_index = ( screen.item_select_index + direction[1] ) % item_count		

	def select_action(self):
		self.control_manager.screen.select_current_action()

	def select_target(self):
		self.control_manager.screen.confirm_current_action()

	def battle_state(self):
		return self.control_manager.screen.mode

SELECT_ACTION = "select_action"
SELECT_TARGET = "select_target"
SELECT_SPELL = "select_spell"
SELECT_ITEM = "select_item"
EXECUTE_ACTIONS = "execute_actions"

BATTLE_MOVE_CURSOR_MAP = {
	SELECT_ACTION:BattleControls.move_action_cursor,
	SELECT_TARGET:BattleControls.move_target_cursor,
	SELECT_ITEM:BattleControls.move_item_cursor
}

BATTLE_ENTER_MAP = {
	SELECT_ACTION:BattleControls.select_action,
	SELECT_TARGET:BattleControls.select_target
}

BATTLE_ESCAPE_MAP = {
	SELECT_TARGET:BattleControls.return_to_action_select,
	SELECT_ITEM:BattleControls.return_to_action_select
}

DIRECTION_MAP = {
	K_LEFT:(-1, 0),
	K_RIGHT:(1, 0),
	K_UP:(0, -1),
	K_DOWN:(0, 1)
}

move_cursor = BattleControls.move_cursor
press_enter = BattleControls.press_enter
press_escape = BattleControls.press_escape

BATTLE_CONTROL_MAP = {
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor,
	K_UP:move_cursor,
	K_DOWN:move_cursor,
	K_RETURN:press_enter,
	K_ESCAPE:press_escape
}