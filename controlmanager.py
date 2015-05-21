class ControlManager:
	""" ControlManager( Controls ) -> ControlManager

	Can hold one Controls object at a time. Uses this to decide what the current input should do.

	Attributes:

	Controls: current control scheme for keyboard input.

	"""

	def __init__(self, controls):
		self.current_controls = controls
		self.current_controls.control_manager = self
		self.screen = None

	def process_event(self, event):
		""" cm.process_event( EVent ) -> None

		Process a keybord/mouse event properly given the current control scheme.
		"""
		self.current_controls.process_event(event)

	def switch_screen(self, screen):
		""" cm.switch_screen( GameScreen ) -> None

		Switch to the given screen.
		"""
		self.screen.switch_screen(screen)

	def switch_controls(self, controls):
		""" cm.switch_controls ( Controls ) -> None

		Change the current control scheme.
		"""
		controls.control_manager = self
		self.current_controls = controls 