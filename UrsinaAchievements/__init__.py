from ursina import *
import os
import json
from direct.stdpy import thread

_path = os.path.dirname(os.path.abspath(__file__))

_achievements_list = []

try:
	with open(f'{_path}/achievements.json', 'r', encoding = 'utf-8') as save_file:
		_achievements_got = json.load(save_file)['achievements_got_names'].copy()
except FileNotFoundError:
	with open(f'{_path}/achievements.json', 'w', encoding = 'utf-8') as save_file:
		_achievements_got = []
		json.dump({'achievements_got_names': []}, save_file, indent = 4)


def create_achievement(name: str, condition, icon: str = None, sound: str = 'sudden', duration: int = 1):

	_achievements_list.append(
		(name, condition, icon, sound, duration)
	)


def _save_achievements():
	with open(f'{_path}/achievements.json', 'w', encoding = 'utf-8') as save_file:
		json.dump({'achievements_got_names': _achievements_got.copy()}, save_file, indent = 2)


class Achievement(Entity):

	# Sounds
	sign = Audio('sounds/sign.wav', autoplay = False, loop = False)
	sudden = Audio('sounds/sudden.wav', autoplay = False, loop = False)
	ringing = Audio('sounds/ringing.wav', autoplay = False, loop = False)
	rising = Audio('sounds/rising.wav', autoplay = False, loop = False)
	sounds = [sign, sudden, ringing, rising]
	
	achievement_color = (64, 64, 64)
	text_color = (255, 255, 255)
	icon_color = (255, 255, 255)

	def __init__(self, title: str, condition, icon: str = None, sound: str = 'sudden', duration: int = 1):
		super().__init__(
			model = 'quad',
			origin = (.5, -.5),
			position = ((.5 * window.aspect_ratio, -.5)),
			scale = (.25, .15),
			color = color.rgba(* Achievement.achievement_color, 185),
			parent = camera.ui,
			always_on_top = True
		)
		# Adding the title
		self.title = Text(
			text = title,
			wordwrap = 15,
			position = (-.95, .9),
			scale = (4, 5.5),
			color = color.rgba(* Achievement.text_color, 255),
			parent = self
		)
		# Adding the icon if wanted
		if icon != None:
			self.icon = Entity(
				model = 'quad',
				texture = icon,
				position = (-.5, .3),
				scale = (.35, .55),
				color = color.rgba(* Achievement.icon_color, 255),
				parent = self
			)

		if sound != None:
			if sound in Achievement.sounds:
				Achievement.sounds[sound].play()
			else:
				Audio(sound, autoplay = True, loop = False)

		# Animation
		prevPos = self.position
		self.position = self.position + Vec2(0, -.2)
		self.animate_position(prevPos, duration = .4 * duration, curve = curve.out_back)
		self.animate_color(color.rgba(* Achievement.achievement_color, 0), duration = 1.5 * duration, delay = 2 * duration)
		self.title.animate_color(color.rgba(* Achievement.text_color, 0), duration = 1.5 * duration, delay = 2 * duration)
		if icon != None:
			self.icon.animate_color(color.rgba(* Achievement.icon_color, 0), duration = 1.5 * duration, delay = 2 * duration)

		invoke(destroy, self, delay = 5 * duration)

def _achievements_update():
	pop = []
	for i, achievement in enumerate(_achievements_list):
		if achievement[1]() is True and achievement[0] not in _achievements_got:
			print(f"You've just achieved: {achievement[0]}")
			Achievement(* achievement)

			# Adds the achievement name to the list of achievements got
			_achievements_got.append(achievement[0])

			# Removes the achievement from the list of achievements to check
			pop.append(i)

			# Saves the achievements got list (new thread)
			try:
				thread.start_new_thread(function = _save_achievements, args = "")

			except Exception as error:
				print('error when saving achievement: ', error)

	for i in range(len(pop)):
		_achievements_list.pop(pop[i] - i)

Entity(update = _achievements_update)

if __name__ == '__main__':

	app = Ursina(borderless = False, fullscreen = True, development_mode = False)

	do = False

	def cond():
		global do
		return do

	create_achievement(name = 'Welcome!', condition = cond, icon = 'confetti', sound = 'sudden', duration = 1.5)

	def setdo():
		global do
		do = True
	invoke(setdo, delay = 3)

	Sky()

	app.run()