from ursina import *
import os
import json
from direct.stdpy import thread
from typing import Callable, Optional, Union, Literal, List
from collections import namedtuple

_path = os.path.dirname(os.path.abspath(__file__))

_achievement_type = namedtuple(
	"AchievementType",
	["name", "condition", "icon", "sound", "duration", "description", "hidden"]
)
_achievements_list: List[_achievement_type] = []

try:
	with open(f'{_path}/achievements.json', 'r', encoding = 'utf-8') as save_file:
		_achievements_got: List[_achievement_type] = json.load(save_file)['achievements_got_names'].copy()
except FileNotFoundError:
	with open(f'{_path}/achievements.json', 'w', encoding = 'utf-8') as save_file:
		_achievements_got: List[_achievement_type] = []
		json.dump({'achievements_got_names': []}, save_file, indent = 4)


def _save_achievements():
	"""
	Internal function.
	Saves the achievements to a file.
	"""
	with open(f'{_path}/achievements.json', 'w', encoding = 'utf-8') as save_file:
		json.dump({'achievements_got_names': _achievements_got.copy()}, save_file, indent = 2)


def create_achievement(
	name: str, condition: Callable[[], Optional[bool]], icon: Optional[str] = None,
	sound: Union[Literal["sign", "sudden", "ringing", "rising"], str] = 'sudden',
	duration: Union[float, int] = 1, description: str = "", hidden: bool = False
):
	"""
	Easy way to create an achievement.
	:param name: The short name of the achievement.
	:param condition: A callback function that will be called every frame to check if the achievement was gotten.
		The achievement will be triggered if the function returns True, and skipped if False or None.
	:param icon: A path to the achievement's icon. If None, no icon will appear for the achievement.
	:param sound: Name of the sound used to signal the achievement get.
		This could be "ringing", "rising", "sign", "sudden" or the path to a WAV format file.
	:param duration: How long the achievement should stay on screen. Please note that this is a multiplier, not a value
		in seconds.
	:param description: A description of the achievement. Will only be displayed in the menus. Empty by default.
	:param hidden: Whether the achievement is a hidden achievement. If True, it will not be shown in the menus unless
		completed previously.
	"""
	# Tests that all the types of the arguments are valid, ensuring type safety.
	if not (
		isinstance(name, str) and callable(condition) and isinstance(icon, Optional[str]) and
		(any(sound.endswith(e) for e in ("sign", "sudden", "ringing", "rising")) or sound.lower().endswith(".wav"))
		and isinstance(duration, Union[float, int]) and isinstance(description, str) and isinstance(hidden, bool)
	):
		raise TypeError("One of the arguments of the function does not have a valid type.")

	# Adds the achievement to the list of achievements
	_achievements_list.append(
		_achievement_type(name, condition, icon, sound, duration, description, hidden)
	)


def achievement(
	name: str, icon: Optional[str] = None,
	sound: Union[Literal["sign", "sudden", "ringing", "rising"], str] = 'sudden',
	duration: Union[float, int] = 1, description: str = "", hidden: bool = False
):
	"""
	Easy way to create an achievement.
	Please define below the decorator a function that will be called every frame to check if the achievement was gotten.
	The achievement will be triggered if the function returns True, and skipped if False or None.
	:param name: The short name of the achievement.
	:param icon: A path to the achievement's icon. If None, no icon will appear for the achievement.
	:param sound: Name of the sound used to signal the achievement get.
		This could be "ringing", "rising", "sign", "sudden" or the path to a WAV format file.
	:param duration: How long the achievement should stay on screen. Please note that this is a multiplier, not a value
		in seconds.
	:param description: A description of the achievement. Will only be displayed in the menus. Empty by default.
	:param hidden: Whether the achievement is a hidden achievement. If True, it will not be shown in the menus unless
		completed previously.
	"""
	def wrap(condition):
		create_achievement(name, condition, icon, sound, duration, description, hidden)
	return wrap


class Achievement(Entity):
	# Sounds
	sign = Audio('sounds/sign.wav', autoplay = False, loop = False)
	sudden = Audio('sounds/sudden.wav', autoplay = False, loop = False)
	ringing = Audio('sounds/ringing.wav', autoplay = False, loop = False)
	rising = Audio('sounds/rising.wav', autoplay = False, loop = False)
	sounds = [sign, sudden, ringing, rising]

	# Colors
	achievement_color = (64, 64, 64)
	text_color = (255, 255, 255)
	icon_color = (255, 255, 255)

	def __init__(
		self, name: str, condition: Callable[[], Optional[bool]], icon: Optional[str] = None,
		sound: Union[Literal["sign", "sudden", "ringing", "rising"], str] = 'sudden',
		duration: Union[float, int] = 1, *_
	):
		"""
		Creates a visual representation of an achievement.
		:param name: The short name of the achievement.
		:param condition: The condition for the achievement to be used. This param will not be used.
		:param icon: A path to the achievement's icon. If None, no icon will appear for the achievement.
		:param sound: Name of the sound used to signal the achievement get.
			This could be "ringing", "rising", "sign", "sudden" or the path to a WAV format file.
		:param duration: How long the achievement should stay on screen. Please note that this is a multiplier, not a value
			in seconds.
		"""
		super().__init__(
			model = 'quad',
			origin = (.5, -.5),
			position = (.5 * window.aspect_ratio, -.5),
			scale = (.25, .15),
			color = color.rgba(*Achievement.achievement_color, 185),
			parent = camera.ui,
			always_on_top = True
		)
		# Adding the title
		self.title = Text(
			text = name,
			wordwrap = 15,
			position = (-.95, .9),
			scale = (4, 5.5),
			color = color.rgba(*Achievement.text_color, 255),
			parent = self
		)
		# Adding the icon if wanted
		if icon is not None:
			self.icon = Entity(
				model = 'quad',
				texture = icon,
				position = (-.5, .3),
				scale = (.35, .55),
				color = color.rgba(*Achievement.icon_color, 255),
				parent = self
			)

		if sound is not None:
			if sound in Achievement.sounds:
				Achievement.sounds[sound].play()
			else:
				Audio(sound, autoplay = True, loop = False)

		# Animation
		prev_pos = self.position
		self.position = self.position + Vec2(0, -.2)
		self.animate_position(prev_pos, duration = .4 * duration, curve = curve.out_back)
		self.animate_color(
			color.rgba(*Achievement.achievement_color, 0), duration = 1.5 * duration, delay = 2 * duration
		)
		self.title.animate_color(
			color.rgba(*Achievement.text_color, 0), duration = 1.5 * duration, delay = 2 * duration
		)
		if icon is not None:
			self.icon.animate_color(
				color.rgba(*Achievement.icon_color, 0), duration = 1.5 * duration, delay = 2 * duration
			)

		invoke(destroy, self, delay = 5 * duration)


def _achievements_update():
	"""
	Internal function.
	Gets called every frame to check for each achievement if it was triggered.
	If so, will show a pop-up to the user.
	"""
	# Creates an empty list of achievements to pop after they have been triggered.
	# Since an achievement will never be triggered twice, this leads to a small memory/performance gain.
	pop = []

	# Loops for each achievement possible
	for i, achievement in enumerate(_achievements_list):
		# If the achievement should be triggered
		if achievement.condition() is True and achievement.name not in _achievements_got:
			# Logs the achievement name and triggers the graphic
			print(f"You've just achieved: {achievement.name}")
			Achievement(*achievement)

			# Adds the achievement name to the list of achievements got
			_achievements_got.append(achievement.name)

			# Removes the achievement from the list of achievements to check
			pop.append(i)

			# Saves the achievements got list (new thread)
			try:
				thread.start_new_thread(function = _save_achievements, args = "")

			except Exception as error:
				print('error when saving achievement: ', error)

	# Removes the triggered achievements from the list of all future possible achievements.
	for i in range(len(pop)):
		_achievements_list.pop(pop[i] - i)


# Makes sure the update method gets called every frame
Entity(update = _achievements_update)

if __name__ == '__main__':

	app = Ursina()

	do = False

	def cond():
		global do
		return do

	create_achievement(name = 'Welcome!', condition = cond, icon = 'textures/confetti.png', sound = 'sudden',
	                   duration = 1.5, description = 'Launch the game !')

	@achievement("Blup!", "textures/bubbles.png", "sign", 1, hidden = True)
	def condition():
		return bool(held_keys["left mouse"])

	@after(1.5)
	def setdo1():
		global do
		do = True

	Sky()

	app.run()
